# src/application/mappers/result_mapper.py


from src.application.dto.calculate_result import (
    CalculateRidgeResultDTO,
    InterpretationDTO,
    RegressionMetricsDTO,
    RidgeParametersDTO,
)
from src.domain.models.regression_result import RegressionResult
from src.domain.services.model_interpreter import ModelInterpreter


class ResultMapper:

    @staticmethod
    def to_dto(result: RegressionResult):

        interpreter = ModelInterpreter()
        interpretation = interpreter.interpret(result)

        return CalculateRidgeResultDTO(
            parameters=RidgeParametersDTO(
                beta=result.parameters.beta,
                alpha=result.parameters.alpha,
                intercept=result.parameters.intercept,
            ),
            metrics=RegressionMetricsDTO(
                mse=result.metrics.mse,
                rmse=result.metrics.rmse,
                mae=result.metrics.mae,
                r2=result.metrics.r2,
            ),
            lambda_beta_used=result.lambda_beta,
            lambda_alpha_used=result.lambda_alpha,
            n_observations=result.n_observations,
            interpretation=InterpretationDTO(
                summary=interpretation.get("house_unit_price_comment", ""),
                quality=interpretation.get("model_quality", ""),
            ),
        )
