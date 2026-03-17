# src/presentation/api/mappers.py


from src.presentation.api.schemas import CalculateRequest, CalculateResponse, InterpretationResponse, ParametersResponse, RegressionMetricsResponse
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
            auto_gamma=request.auto_gamma,
            gamma=request.gamma,
        )


class ResponseMapper:

    @staticmethod
    def from_dto(dto) -> CalculateResponse:
        return CalculateResponse(
            parameters=ParametersResponse(
                beta=dto.parameters.beta,
                alpha=dto.parameters.alpha,
                intercept=dto.parameters.intercept,
            ),
            metrics=RegressionMetricsResponse(
                mse=dto.metrics.mse,
                rmse=dto.metrics.rmse,
                mae=dto.metrics.mae,
                r2=dto.metrics.r2,
            ),
            gamma_used=dto.gamma_used,
            n_observations=dto.n_observations,
            interpretation=InterpretationResponse(
                summary=dto.interpretation.summary,
                quality=dto.interpretation.quality,
            ),
        )
