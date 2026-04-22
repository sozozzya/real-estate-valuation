# src/application/factories/gamma_strategy_factory.py


from src.domain.exceptions import ValidationError
from src.domain.services.gamma_strategy import (
    FixedGammaStrategy,
    VarianceBasedGammaStrategy,
)
from typing import Optional


class GammaStrategyFactory:

    @staticmethod
    def create(
        auto_lambda: bool,
        lambda_value: Optional[float],
    ):

        if auto_lambda:
            return VarianceBasedGammaStrategy(scale=0.01)

        if lambda_value is None:
            raise ValidationError(
                "lambda_value must be provided when auto_lambda is False"
            )

        return FixedGammaStrategy(lambda_beta=lambda_value, lambda_alpha=lambda_value)
