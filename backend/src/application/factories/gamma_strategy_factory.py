# src/application/factories/gamma_strategy_factory.py


from src.domain.exceptions import ValidationError
from src.domain.services.gamma_strategy import (
    FixedGammaStrategy,
    VarianceBasedGammaStrategy,
)
from typing import Optional


class GammaStrategyFactory:

    @staticmethod
    def create(auto_gamma: bool, gamma: Optional[float]):

        if auto_gamma:
            return VarianceBasedGammaStrategy(scale=0.01)

        if gamma is None:
            raise ValidationError(
                "gamma must be provided when auto_gamma is False")

        return FixedGammaStrategy(gamma)
