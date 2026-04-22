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
        lambda_beta: Optional[float],
        lambda_alpha: Optional[float],
    ):

        if auto_lambda:
            return VarianceBasedGammaStrategy(scale=0.01)

        if lambda_beta is None or lambda_alpha is None:
            raise ValidationError(
                "lambda_beta and lambda_alpha must be provided when auto_lambda is False"
            )

        return FixedGammaStrategy(lambda_beta=lambda_beta, lambda_alpha=lambda_alpha)
