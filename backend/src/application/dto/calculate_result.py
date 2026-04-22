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


@dataclass(frozen=True)
class ConfidenceIntervalDTO:
    lower: float
    upper: float


@dataclass(frozen=True)
class UncertaintyDTO:
    beta_ci_95: ConfidenceIntervalDTO
    alpha_ci_95: ConfidenceIntervalDTO


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
    behavior: str
    market_change: str
    reliability: str


@dataclass(frozen=True)
class CvPointDTO:
    lambda_value: float
    loocv_mse: float


@dataclass(frozen=True)
class SplitInfoDTO:
    train_size: int
    test_size: int


@dataclass(frozen=True)
class CalculateRidgeResultDTO:
    parameters: RidgeParametersDTO
    metrics: RegressionMetricsDTO
    uncertainty: UncertaintyDTO
    lambda_star: float
    split: SplitInfoDTO
    cv_curve: list[CvPointDTO]
    prediction_formula: str
    n_observations: int
    interpretation: InterpretationDTO
