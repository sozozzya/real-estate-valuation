# src/application/dto/calculate_result.py

from dataclasses import dataclass


@dataclass(frozen=True)
class RidgeParametersDTO:
    beta: float
    alpha: float
    intercept: float


@dataclass(frozen=True)
class RegressionMetricsDTO:
    mse: float
    rmse: float
    mae: float
    r2: float


@dataclass(frozen=True)
class InterpretationDTO:
    summary: str
    quality: str


@dataclass(frozen=True)
class CalculateRidgeResultDTO:
    parameters: RidgeParametersDTO
    metrics: RegressionMetricsDTO
    lambda_beta_used: float
    lambda_alpha_used: float
    n_observations: int
    interpretation: InterpretationDTO
