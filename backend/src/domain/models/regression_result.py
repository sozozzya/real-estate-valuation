# src/domain/models/regression_result.py

from dataclasses import dataclass
from typing import Optional

from src.domain.models.ridge_parameters import RidgeParameters
from src.domain.services.metrics import RegressionMetrics
from src.domain.services.uncertainty_estimator import ParameterUncertainty


@dataclass(frozen=True)
class RegressionResult:
    parameters: RidgeParameters
    metrics: RegressionMetrics
    uncertainty: ParameterUncertainty
    lambda_beta: float
    lambda_alpha: float
    beta_prior: Optional[float]
    alpha_prior: Optional[float]
    prediction_formula: str
    n_observations: int
