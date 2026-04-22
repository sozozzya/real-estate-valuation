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
    lambda_beta: Optional[float] = None
    lambda_alpha: Optional[float] = None

    @model_validator(mode="after")
    def validate_lambda(self):
        if not self.auto_lambda and (self.lambda_beta is None or self.lambda_alpha is None):
            raise ValueError("lambda_beta and lambda_alpha must be provided if auto_lambda is False")
        return self

    @model_validator(mode="after")
    def validate_properties(self):
        if len(self.properties) < 5:
            raise ValueError("At least five properties are required for train/test split and LOOCV")
        return self


class RegressionMetricsResponse(BaseModel):
    mse: float
    rmse: float
    mae: float


class ParametersResponse(BaseModel):
    beta: float
    alpha: float


class ConfidenceIntervalResponse(BaseModel):
    lower: float
    upper: float


class UncertaintyResponse(BaseModel):
    beta_ci_95: ConfidenceIntervalResponse
    alpha_ci_95: ConfidenceIntervalResponse


class InterpretationResponse(BaseModel):
    behavior: str
    market_change: str
    reliability: str


class CvPointResponse(BaseModel):
    lambda_value: float
    loocv_mse: float


class SplitInfoResponse(BaseModel):
    train_size: int
    test_size: int


class CalculateResponse(BaseModel):
    parameters: ParametersResponse
    metrics: RegressionMetricsResponse
    uncertainty: UncertaintyResponse
    lambda_star: float
    split: SplitInfoResponse
    cv_curve: List[CvPointResponse]
    prediction_formula: str
    n_observations: int
    interpretation: InterpretationResponse
