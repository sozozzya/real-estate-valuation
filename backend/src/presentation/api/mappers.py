from src.presentation.api.schemas import (
    CalculateRequest,
    CalculateResponse,
    ConfidenceIntervalResponse,
    CvPointResponse,
    InterpretationResponse,
    ParametersResponse,
    RegressionMetricsResponse,
    SplitInfoResponse,
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
                mse=dto.metrics.mse,
                rmse=dto.metrics.rmse,
                mae=dto.metrics.mae,
            ),
            uncertainty=UncertaintyResponse(
                beta_ci_95=ConfidenceIntervalResponse(
                    lower=dto.uncertainty.beta_ci_95.lower,
                    upper=dto.uncertainty.beta_ci_95.upper,
                ),
                alpha_ci_95=ConfidenceIntervalResponse(
                    lower=dto.uncertainty.alpha_ci_95.lower,
                    upper=dto.uncertainty.alpha_ci_95.upper,
                ),
            ),
            lambda_star=dto.lambda_star,
            split=SplitInfoResponse(
                train_size=dto.split.train_size,
                test_size=dto.split.test_size,
            ),
            cv_curve=[
                CvPointResponse(lambda_value=p.lambda_value, loocv_mse=p.loocv_mse)
                for p in dto.cv_curve
            ],
            prediction_formula=dto.prediction_formula,
            n_observations=dto.n_observations,
            interpretation=InterpretationResponse(
                behavior=dto.interpretation.behavior,
                market_change=dto.interpretation.market_change,
                reliability=dto.interpretation.reliability,
            ),
        )
