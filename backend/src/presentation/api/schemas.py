from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


class PropertyRequest(BaseModel):
    price: float = Field(..., gt=0)
    house_area: float = Field(..., gt=0)
    land_area: float = Field(..., gt=0)


class CalculateRequest(BaseModel):
    properties: List[PropertyRequest]

    beta_prior: Optional[float] = None
    alpha_prior: Optional[float] = None

    auto_lambda: bool = True
    lambda_value: Optional[float] = None

    @model_validator(mode="after")
    def validate_lambda(self):
        if not self.auto_lambda and self.lambda_value is None:
            raise ValueError("lambda_value must be provided if auto_lambda is False")
        if self.lambda_value is not None and self.lambda_value <= 0:
            raise ValueError("lambda_value must be positive")
        return self

    @model_validator(mode="after")
    def validate_properties(self):
        if len(self.properties) < 5:
            raise ValueError("At least five properties are required")
        return self


class RegressionMetricsResponse(BaseModel):
    r2_loocv: float
    rmse_loocv: float
    mae_loocv: float
    mape_loocv: float


class ParametersResponse(BaseModel):
    beta: float
    alpha: float


class ConfidenceIntervalResponse(BaseModel):
    lower: float
    upper: float


class UncertaintyResponse(BaseModel):
    beta_ci_95: ConfidenceIntervalResponse
    alpha_ci_95: ConfidenceIntervalResponse
    beta_shift_pct: float
    alpha_shift_pct: float
    regularization_strength: str


class InterpretationResponse(BaseModel):
    behavior: str
    regularization_impact: str
    market_change: str
    forecast_reliability: str
    limitations: str


class CvPointResponse(BaseModel):
    lambda_value: float
    loocv_mse: float


class DiagnosticsResponse(BaseModel):
    mean_residual: float


class CalculateResponse(BaseModel):
    parameters: ParametersResponse
    metrics: RegressionMetricsResponse
    uncertainty: UncertaintyResponse
    lambda_star: float
    cv_curve: List[CvPointResponse]
    diagnostics: DiagnosticsResponse
    prediction_formula: str
    n_observations: int
    interpretation: InterpretationResponse
