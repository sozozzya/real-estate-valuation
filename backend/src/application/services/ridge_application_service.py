import logging

import numpy as np

from src.application.dto.calculate_result import (
    CalculateRidgeResultDTO,
    ConfidenceIntervalDTO,
    CvPointDTO,
    DiagnosticsDTO,
    InterpretationDTO,
    RegressionMetricsDTO,
    RidgeParametersDTO,
    UncertaintyDTO,
)
from src.domain.exceptions import DomainError

logger = logging.getLogger("ridge_application_service")


class RidgeApplicationService:

    _DEFAULT_GRID = [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]

    @staticmethod
    def _fit_theta(X: np.ndarray, y: np.ndarray, prior: np.ndarray, lam: float) -> np.ndarray:
        return np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ y + lam * prior)

    @staticmethod
    def _scale_by_std(X: np.ndarray):
        std = np.std(X, axis=0)
        std = np.where(std < 1e-8, 1.0, std)
        return X / std, std

    def _loocv_predictions(self, X: np.ndarray, y: np.ndarray, prior: np.ndarray, lam: float) -> np.ndarray:
        n = X.shape[0]
        preds = np.zeros(n, dtype=float)
        for i in range(n):
            mask = np.ones(n, dtype=bool)
            mask[i] = False
            theta = self._fit_theta(X[mask], y[mask], prior, lam)
            preds[i] = float(X[i] @ theta)
        return preds

    @staticmethod
    def _reg_strength(lam: float) -> str:
        if lam < 0.1:
            return "слабая"
        if lam <= 1.0:
            return "умеренная"
        return "сильная"

    def execute(self, input_dto):
        logger.info("ridge_application_service_started", extra={"n_properties": len(input_dto.properties)})

        try:
            X_raw = np.array([[p.house_area, p.land_area] for p in input_dto.properties], dtype=float)
            y = np.array([p.price for p in input_dto.properties], dtype=float)

            X, std = self._scale_by_std(X_raw)

            beta0 = float(input_dto.beta_prior or 0.0)
            alpha0 = float(input_dto.alpha_prior or 0.0)
            prior_scaled = np.array([beta0, alpha0], dtype=float) * std

            if input_dto.auto_lambda:
                grid = self._DEFAULT_GRID
            else:
                grid = [float(input_dto.lambda_value)]

            cv_curve: list[CvPointDTO] = []
            best_lambda = grid[0]
            best_loocv_mse = float("inf")
            best_preds = None

            for lam in grid:
                preds = self._loocv_predictions(X, y, prior_scaled, lam)
                mse = float(np.mean((y - preds) ** 2))
                cv_curve.append(CvPointDTO(lambda_value=float(lam), loocv_mse=mse))
                if mse < best_loocv_mse:
                    best_loocv_mse = mse
                    best_lambda = float(lam)
                    best_preds = preds

            assert best_preds is not None

            final_theta = self._fit_theta(X, y, prior_scaled, best_lambda)
            beta = float(final_theta[0] / std[0])
            alpha = float(final_theta[1] / std[1])

            residuals = y - best_preds
            mse = float(np.mean(residuals ** 2))
            rmse = float(np.sqrt(mse))
            mae = float(np.mean(np.abs(residuals)))
            safe = np.where(np.abs(y) < 1e-8, 1e-8, y)
            mape = float(np.mean(np.abs(residuals / safe)) * 100)
            ss_tot = float(np.sum((y - np.mean(y)) ** 2))
            r2 = 0.0 if ss_tot == 0 else float(1 - np.sum(residuals ** 2) / ss_tot)

            dof = max(len(y) - 2, 1)
            sigma2 = float(np.sum((y - (X_raw @ np.array([beta, alpha]))) ** 2) / dof)
            cov = sigma2 * np.linalg.inv(X_raw.T @ X_raw + best_lambda * np.eye(2))
            se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
            beta_ci = ConfidenceIntervalDTO(lower=float(beta - 1.96 * se[0]), upper=float(beta + 1.96 * se[0]))
            alpha_ci = ConfidenceIntervalDTO(lower=float(alpha - 1.96 * se[1]), upper=float(alpha + 1.96 * se[1]))

            beta_shift = 0.0 if abs(beta0) < 1e-8 else float((beta - beta0) / beta0 * 100)
            alpha_shift = 0.0 if abs(alpha0) < 1e-8 else float((alpha - alpha0) / alpha0 * 100)

            reliability_msg = (
                "Модель демонстрирует стабильную точность, однако разброс данных указывает на умеренную неопределённость оценок."
                if rmse < np.mean(y) * 0.25
                else "Точность модели ограничена высоким разбросом данных; неопределённость оценок повышена."
            )

            result = CalculateRidgeResultDTO(
                parameters=RidgeParametersDTO(beta=beta, alpha=alpha),
                metrics=RegressionMetricsDTO(r2_loocv=r2, rmse_loocv=rmse, mae_loocv=mae, mape_loocv=mape),
                uncertainty=UncertaintyDTO(
                    beta_ci_95=beta_ci,
                    alpha_ci_95=alpha_ci,
                    beta_shift_pct=beta_shift,
                    alpha_shift_pct=alpha_shift,
                    regularization_strength=self._reg_strength(best_lambda),
                ),
                lambda_star=best_lambda,
                cv_curve=cv_curve,
                diagnostics=DiagnosticsDTO(mean_residual=float(np.mean(residuals))),
                prediction_formula=f"V = {beta:.4f} * S + {alpha:.4f} * Q",
                n_observations=int(len(y)),
                interpretation=InterpretationDTO(
                    behavior=(
                        "Новые данные имеют высокий разброс, поэтому модель частично опирается на предыдущий период."
                        if best_lambda >= 1
                        else "Новые данные стабильны, модель в основном опирается на текущие наблюдения."
                    ),
                    regularization_impact="Модель частично опирается на оценки предыдущего периода, что повышает устойчивость при малом объёме данных.",
                    market_change=f"Изменение к прошлому периоду: дом {beta_shift:+.1f}%, участок {alpha_shift:+.1f}%.",
                    forecast_reliability=reliability_msg,
                    limitations="Модель учитывает только площадь дома и участка и не учитывает локацию, состояние и иные факторы.",
                ),
            )

            logger.info("ridge_application_service_completed", extra={"lambda_star": best_lambda, "rmse_loocv": rmse})
            return result

        except DomainError:
            logger.warning("ridge_application_service_domain_error", exc_info=True)
            raise
        except Exception:
            logger.exception("ridge_application_service_unexpected_error")
            raise
