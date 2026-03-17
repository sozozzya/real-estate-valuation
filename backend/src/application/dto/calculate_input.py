# src/application/dto/calculate_input.py

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class PropertyInputDTO:
    price: float
    house_area: float
    land_area: float


@dataclass(frozen=True)
class CalculateRidgeInputDTO:
    properties: List[PropertyInputDTO]

    # prior (optional)
    beta_prior: Optional[float] = None
    alpha_prior: Optional[float] = None

    # regularization logic
    auto_lambda: bool = True
    lambda_beta: Optional[float] = None
    lambda_alpha: Optional[float] = None
