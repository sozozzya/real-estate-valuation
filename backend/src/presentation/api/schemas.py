# src/presentation/api/schemas.py

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
        if len(self.properties) < 2:
            raise ValueError("At least two properties are required")
        return self


class RegressionMetricsResponse(BaseModel):
    mse: float
    rmse: float
    mae: float
    r2: float


class ParametersResponse(BaseModel):
    beta: float
    alpha: float
    intercept: float


class InterpretationResponse(BaseModel):
    summary: str
    quality: str


class CalculateResponse(BaseModel):
    parameters: ParametersResponse
    metrics: RegressionMetricsResponse
    lambda_beta_used: float
    lambda_alpha_used: float
    n_observations: int
    interpretation: InterpretationResponse
