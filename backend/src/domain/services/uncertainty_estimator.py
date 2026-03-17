# src/domain/services/uncertainty_estimator.py

from dataclasses import dataclass

import numpy as np

from src.domain.models.ridge_parameters import RidgeParameters


@dataclass(frozen=True)
class ParameterInterval:
    lower: float
    upper: float


@dataclass(frozen=True)
class ParameterUncertainty:
    beta_se: float
    alpha_se: float
    beta_ci_95: ParameterInterval
    alpha_ci_95: ParameterInterval


class UncertaintyEstimator:

    _Z_95 = 1.96

    def estimate(
        self,
        X: np.ndarray,
        y: np.ndarray,
        params: RidgeParameters,
        lambda_beta: float,
        lambda_alpha: float,
    ) -> ParameterUncertainty:

        theta = params.as_vector()
        y_pred = X @ theta
        residuals = y - y_pred

        n = X.shape[0]
        p = X.shape[1]
        dof = max(n - p, 1)
        sigma2 = float(np.sum(residuals**2) / dof)

        xtx = X.T @ X
        lambda_matrix = np.diag([lambda_beta, lambda_alpha])
        inv_term = np.linalg.inv(xtx + lambda_matrix)

        covariance = sigma2 * inv_term @ xtx @ inv_term
        se = np.sqrt(np.clip(np.diag(covariance), 0.0, None))

        beta_se = float(se[0])
        alpha_se = float(se[1])

        beta_interval = ParameterInterval(
            lower=float(params.beta - self._Z_95 * beta_se),
            upper=float(params.beta + self._Z_95 * beta_se),
        )

        alpha_interval = ParameterInterval(
            lower=float(params.alpha - self._Z_95 * alpha_se),
            upper=float(params.alpha + self._Z_95 * alpha_se),
        )

        return ParameterUncertainty(
            beta_se=beta_se,
            alpha_se=alpha_se,
            beta_ci_95=beta_interval,
            alpha_ci_95=alpha_interval,
        )
