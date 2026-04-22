# src/domain/services/metrics.py

import numpy as np
from dataclasses import dataclass

from src.domain.models.ridge_parameters import RidgeParameters


@dataclass(frozen=True)
class RegressionMetrics:

    rss: float
    mse: float
    rmse: float
    mae: float
    mape: float
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

        rss = float(np.sum(residuals**2))
        mse = float(np.mean(residuals**2))
        rmse = float(np.sqrt(mse))
        mae = float(np.mean(np.abs(residuals)))

        safe_actual = np.where(np.abs(y) < 1e-12, 1e-12, y)
        mape = float(np.mean(np.abs(residuals / safe_actual)) * 100)

        ss_total = np.sum((y - np.mean(y)) ** 2)
        r2 = 0.0 if ss_total == 0 else float(1 - rss / ss_total)

        return RegressionMetrics(
            rss=rss,
            mse=mse,
            rmse=rmse,
            mae=mae,
            mape=mape,
            r2=r2,
        )
