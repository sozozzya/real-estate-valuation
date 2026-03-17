# src/domain/services/metrics.py

import numpy as np
from dataclasses import dataclass

from src.domain.models.ridge_parameters import RidgeParameters


@dataclass(frozen=True)
class RegressionMetrics:

    mse: float
    rmse: float
    mae: float
    r2: float


class MetricsCalculator:

    def calculate(
        self,
        X: np.ndarray,
        y: np.ndarray,
        params: RidgeParameters,
    ) -> RegressionMetrics:

        theta = params.as_vector()

        y_pred = X @ theta

        residuals = y - y_pred

        mse = float(np.mean(residuals**2))
        rmse = float(np.sqrt(mse))
        mae = float(np.mean(np.abs(residuals)))

        ss_total = np.sum((y - np.mean(y)) ** 2)
        ss_res = np.sum(residuals**2)

        r2 = 0.0 if ss_total == 0 else float(1 - ss_res / ss_total)

        return RegressionMetrics(
            mse=mse,
            rmse=rmse,
            mae=mae,
            r2=r2,
        )
