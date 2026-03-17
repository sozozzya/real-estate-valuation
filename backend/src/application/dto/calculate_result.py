# src/application/dto/calculate_result.py

from dataclasses import dataclass


@dataclass(frozen=True)
class RidgeParametersDTO:
    beta: float
    alpha: float


@dataclass(frozen=True)
class RegressionMetricsDTO:
    rss: float
    mse: float
    rmse: float
    mae: float
    mape: float
    r2: float


@dataclass(frozen=True)
class ConfidenceIntervalDTO:
    lower: float
    upper: float


@dataclass(frozen=True)
class UncertaintyDTO:
    beta_standard_error: float
    alpha_standard_error: float
    beta_ci_95: ConfidenceIntervalDTO
    alpha_ci_95: ConfidenceIntervalDTO


@dataclass(frozen=True)
class InterpretationDTO:
    summary: str
    quality: str


@dataclass(frozen=True)
class CalculateRidgeResultDTO:
    parameters: RidgeParametersDTO
    metrics: RegressionMetricsDTO
    uncertainty: UncertaintyDTO
    lambda_beta_used: float
    lambda_alpha_used: float
    prediction_formula: str
    n_observations: int
    interpretation: InterpretationDTO
