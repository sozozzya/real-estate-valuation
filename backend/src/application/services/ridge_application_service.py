import logging
from dataclasses import asdict

import numpy as np

from src.application.dto.calculate_result import (
    CalculateRidgeResultDTO,
    ConfidenceIntervalDTO,
    CvPointDTO,
    InterpretationDTO,
    RegressionMetricsDTO,
    RidgeParametersDTO,
    SplitInfoDTO,
    UncertaintyDTO,
)
from src.domain.exceptions import DomainError

logger = logging.getLogger("ridge_application_service")


class RidgeApplicationService:

    _DEFAULT_GRID = [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]

    @staticmethod
    def _train_test_split(X: np.ndarray, y: np.ndarray, test_ratio: float = 0.2):
        n = X.shape[0]
        test_size = max(1, int(round(n * test_ratio)))
        rng = np.random.default_rng(42)
        idx = np.arange(n)
        rng.shuffle(idx)
        test_idx = idx[:test_size]
        train_idx = idx[test_size:]
        return X[train_idx], y[train_idx], X[test_idx], y[test_idx]

    @staticmethod
    def _fit_theta(X: np.ndarray, y: np.ndarray, prior: np.ndarray, lam: float):
        A = X.T @ X + lam * np.eye(X.shape[1])
        b = X.T @ y + lam * prior
        return np.linalg.solve(A, b)

    def _loocv_error(self, X: np.ndarray, y: np.ndarray, prior: np.ndarray, lam: float) -> float:
        n = X.shape[0]
        errors = []
        for i in range(n):
            mask = np.ones(n, dtype=bool)
            mask[i] = False
            theta = self._fit_theta(X[mask], y[mask], prior, lam)
            pred = float(X[i] @ theta)
            errors.append((float(y[i]) - pred) ** 2)
        return float(np.mean(errors))

    @staticmethod
    def _scale_by_std(X_train: np.ndarray, X_other: np.ndarray):
        std = np.std(X_train, axis=0)
        std = np.where(std < 1e-8, 1.0, std)
        return X_train / std, X_other / std, std

    def execute(self, input_dto):

        logger.info(
            "ridge_application_service_started",
            extra={"n_properties": len(input_dto.properties), "auto_lambda": input_dto.auto_lambda},
        )

        try:
            X = np.array([[p.house_area, p.land_area] for p in input_dto.properties], dtype=float)
            y = np.array([p.price for p in input_dto.properties], dtype=float)

            X_train, y_train, X_test, y_test = self._train_test_split(X, y, test_ratio=0.2)

            X_train_s, X_test_s, std = self._scale_by_std(X_train, X_test)

            beta0 = 0.0 if input_dto.beta_prior is None else float(input_dto.beta_prior)
            alpha0 = 0.0 if input_dto.alpha_prior is None else float(input_dto.alpha_prior)
            prior_raw = np.array([beta0, alpha0], dtype=float)
            prior_s = prior_raw * std

            if input_dto.auto_lambda:
                grid = self._DEFAULT_GRID
            else:
                manual_lambda = float((input_dto.lambda_beta + input_dto.lambda_alpha) / 2.0)
                grid = [manual_lambda]

            cv_points = []
            best_lambda = grid[0]
            best_error = float("inf")

            for lam in grid:
                cv_err = self._loocv_error(X_train_s, y_train, prior_s, lam)
                cv_points.append(CvPointDTO(lambda_value=float(lam), loocv_mse=float(cv_err)))
                if cv_err < best_error:
                    best_error = cv_err
                    best_lambda = float(lam)

            theta_s = self._fit_theta(X_train_s, y_train, prior_s, best_lambda)
            beta = float(theta_s[0] / std[0])
            alpha = float(theta_s[1] / std[1])

            y_pred = X_test @ np.array([beta, alpha], dtype=float)
            residuals = y_test - y_pred

            mse = float(np.mean(residuals ** 2))
            rmse = float(np.sqrt(mse))
            mae = float(np.mean(np.abs(residuals)))

            # simple CI approximation via train residual variance
            train_pred = X_train @ np.array([beta, alpha], dtype=float)
            train_resid = y_train - train_pred
            dof = max(len(y_train) - 2, 1)
            sigma2 = float(np.sum(train_resid ** 2) / dof)
            cov = sigma2 * np.linalg.inv(X_train.T @ X_train + best_lambda * np.eye(2))
            se_beta, se_alpha = np.sqrt(np.clip(np.diag(cov), 0.0, None))

            beta_ci = ConfidenceIntervalDTO(lower=float(beta - 1.96 * se_beta), upper=float(beta + 1.96 * se_beta))
            alpha_ci = ConfidenceIntervalDTO(lower=float(alpha - 1.96 * se_alpha), upper=float(alpha + 1.96 * se_alpha))

            quality_label = "слабое" if mse > 0 and rmse > np.mean(y_test) * 0.3 else "хорошее"

            result = CalculateRidgeResultDTO(
                parameters=RidgeParametersDTO(beta=beta, alpha=alpha),
                metrics=RegressionMetricsDTO(mse=mse, rmse=rmse, mae=mae),
                uncertainty=UncertaintyDTO(beta_ci_95=beta_ci, alpha_ci_95=alpha_ci),
                lambda_star=best_lambda,
                split=SplitInfoDTO(train_size=int(len(y_train)), test_size=int(len(y_test))),
                cv_curve=cv_points,
                prediction_formula=f"V = {beta:.4f} * S + {alpha:.4f} * Q",
                n_observations=int(len(y)),
                interpretation=InterpretationDTO(
                    behavior=(
                        "Новые данные имеют высокий разброс, модель использует компромисс между историей и текущим рынком."
                        if best_lambda >= 1
                        else "Новые данные стабильны, модель преимущественно опирается на текущую выборку."
                    ),
                    market_change=(
                        f"Относительно приора: дом {'вырос' if beta >= beta0 else 'снизился'}, участок {'вырос' if alpha >= alpha0 else 'снизился'}."
                    ),
                    reliability=(
                        "Оценки параметров стабильны." if (beta_ci.upper - beta_ci.lower + alpha_ci.upper - alpha_ci.lower) < abs(beta + alpha) * 0.5
                        else "Оценки имеют повышенную неопределённость из-за малого объёма данных."
                    ),
                ),
            )

            logger.info("ridge_application_service_completed", extra={"lambda_star": best_lambda, "mse_test": mse})
            return result

        except DomainError:
            logger.warning("ridge_application_service_domain_error", exc_info=True)
            raise
        except Exception:
            logger.exception("ridge_application_service_unexpected_error")
            raise
