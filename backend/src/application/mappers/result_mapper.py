# src/application/mappers/result_mapper.py


from src.application.dto.calculate_result import (
    CalculateRidgeResultDTO,
    ConfidenceIntervalDTO,
    InterpretationDTO,
    RegressionMetricsDTO,
    RidgeParametersDTO,
    UncertaintyDTO,
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
            ),
            metrics=RegressionMetricsDTO(
                rss=result.metrics.rss,
                mse=result.metrics.mse,
                rmse=result.metrics.rmse,
                mae=result.metrics.mae,
                mape=result.metrics.mape,
                r2=result.metrics.r2,
            ),
            uncertainty=UncertaintyDTO(
                beta_standard_error=result.uncertainty.beta_se,
                alpha_standard_error=result.uncertainty.alpha_se,
                beta_ci_95=ConfidenceIntervalDTO(
                    lower=result.uncertainty.beta_ci_95.lower,
                    upper=result.uncertainty.beta_ci_95.upper,
                ),
                alpha_ci_95=ConfidenceIntervalDTO(
                    lower=result.uncertainty.alpha_ci_95.lower,
                    upper=result.uncertainty.alpha_ci_95.upper,
                ),
            ),
            lambda_beta_used=result.lambda_beta,
            lambda_alpha_used=result.lambda_alpha,
            prediction_formula=result.prediction_formula,
            n_observations=result.n_observations,
            interpretation=InterpretationDTO(
                summary=interpretation.get("summary", ""),
                quality=interpretation.get("model_quality", ""),
            ),
        )
