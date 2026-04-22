from dataclasses import dataclass, field


@dataclass(frozen=True)
class RidgeParametersDTO:
    beta: float
    alpha: float


@dataclass(frozen=True)
class RegressionMetricsDTO:
    # Backward-compatible fields
    rss: float = 0.0
    mse: float = 0.0
    rmse: float = 0.0
    mae: float = 0.0
    mape: float = 0.0
    r2: float = 0.0

    # Production LOOCV fields
    r2_loocv: float = 0.0
    rmse_loocv: float = 0.0
    mae_loocv: float = 0.0
    mape_loocv: float = 0.0


@dataclass(frozen=True)
class ConfidenceIntervalDTO:
    lower: float
    upper: float


@dataclass(frozen=True)
class UncertaintyDTO:
    beta_ci_95: ConfidenceIntervalDTO
    alpha_ci_95: ConfidenceIntervalDTO
    beta_shift_pct: float = 0.0
    alpha_shift_pct: float = 0.0
    regularization_strength: str = "умеренная"


@dataclass(frozen=True)
class InterpretationDTO:
    behavior: str
    regularization_impact: str = ""
    market_change: str = ""
    forecast_reliability: str = ""
    limitations: str = ""


@dataclass(frozen=True)
class CvPointDTO:
    lambda_value: float
    loocv_mse: float


@dataclass(frozen=True)
class DiagnosticsDTO:
    mean_residual: float = 0.0


@dataclass(frozen=True)
class CalculateRidgeResultDTO:
    parameters: RidgeParametersDTO
    metrics: RegressionMetricsDTO
    uncertainty: UncertaintyDTO
    lambda_star: float
    cv_curve: list[CvPointDTO] = field(default_factory=list)
    diagnostics: DiagnosticsDTO = field(default_factory=DiagnosticsDTO)
    prediction_formula: str = ""
    n_observations: int = 0
    interpretation: InterpretationDTO = field(default_factory=lambda: InterpretationDTO(behavior=""))
