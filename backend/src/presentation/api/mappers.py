# src/presentation/api/mappers.py


from src.presentation.api.schemas import (
    CalculateRequest,
    CalculateResponse,
    ConfidenceIntervalResponse,
    InterpretationResponse,
    ParametersResponse,
    RegressionMetricsResponse,
    UncertaintyResponse,
)
from src.application.dto.calculate_input import (
    CalculateRidgeInputDTO,
    PropertyInputDTO,
)


class RequestMapper:

    @staticmethod
    def to_dto(request: CalculateRequest) -> CalculateRidgeInputDTO:

        return CalculateRidgeInputDTO(
            properties=[
                PropertyInputDTO(
                    price=p.price,
                    house_area=p.house_area,
                    land_area=p.land_area,
                )
                for p in request.properties
            ],
            beta_prior=request.beta_prior,
            alpha_prior=request.alpha_prior,
            auto_lambda=request.auto_lambda,
            lambda_beta=request.lambda_beta,
            lambda_alpha=request.lambda_alpha,
        )


class ResponseMapper:

    @staticmethod
    def from_dto(dto) -> CalculateResponse:
        return CalculateResponse(
            parameters=ParametersResponse(
                beta=dto.parameters.beta,
                alpha=dto.parameters.alpha,
            ),
            metrics=RegressionMetricsResponse(
                rss=dto.metrics.rss,
                mse=dto.metrics.mse,
                rmse=dto.metrics.rmse,
                mae=dto.metrics.mae,
                mape=dto.metrics.mape,
                r2=dto.metrics.r2,
            ),
<<<<<<< HEAD
            uncertainty=UncertaintyResponse(
                beta_standard_error=dto.uncertainty.beta_standard_error,
                alpha_standard_error=dto.uncertainty.alpha_standard_error,
                beta_ci_95=ConfidenceIntervalResponse(
                    lower=dto.uncertainty.beta_ci_95.lower,
                    upper=dto.uncertainty.beta_ci_95.upper,
                ),
                alpha_ci_95=ConfidenceIntervalResponse(
                    lower=dto.uncertainty.alpha_ci_95.lower,
                    upper=dto.uncertainty.alpha_ci_95.upper,
                ),
            ),
            lambda_beta_used=dto.lambda_beta_used,
            lambda_alpha_used=dto.lambda_alpha_used,
            prediction_formula=dto.prediction_formula,
=======
            lambda_beta_used=dto.lambda_beta_used,
            lambda_alpha_used=dto.lambda_alpha_used,
>>>>>>> main
            n_observations=dto.n_observations,
            interpretation=InterpretationResponse(
                summary=dto.interpretation.summary,
                quality=dto.interpretation.quality,
            ),
        )
