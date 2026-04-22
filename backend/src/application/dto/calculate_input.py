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

    beta_prior: Optional[float] = None
    alpha_prior: Optional[float] = None

    auto_lambda: bool = True
    lambda_value: Optional[float] = None
