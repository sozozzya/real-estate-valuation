# src/domain/models/regression_result.py

from dataclasses import dataclass

from src.domain.models.ridge_parameters import RidgeParameters
from src.domain.services.metrics import RegressionMetrics


@dataclass(frozen=True)
class RegressionResult:
    parameters: RidgeParameters
    metrics: RegressionMetrics
    lambda_beta: float
    lambda_alpha: float
    n_observations: int
