from src.presentation.api.schemas import (
    CalculateRequest,
    CalculateResponse,
    ConfidenceIntervalResponse,
    CvPointResponse,
    DiagnosticsResponse,
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
            lambda_value=request.lambda_value,
        )


class ResponseMapper:

    @staticmethod
    def from_dto(dto) -> CalculateResponse:
        return CalculateResponse(
            parameters=ParametersResponse(beta=dto.parameters.beta, alpha=dto.parameters.alpha),
            metrics=RegressionMetricsResponse(
                r2_loocv=dto.metrics.r2_loocv,
                rmse_loocv=dto.metrics.rmse_loocv,
                mae_loocv=dto.metrics.mae_loocv,
                mape_loocv=dto.metrics.mape_loocv,
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
                beta_shift_pct=dto.uncertainty.beta_shift_pct,
                alpha_shift_pct=dto.uncertainty.alpha_shift_pct,
                regularization_strength=dto.uncertainty.regularization_strength,
            ),
            lambda_star=dto.lambda_star,
            cv_curve=[CvPointResponse(lambda_value=p.lambda_value, loocv_mse=p.loocv_mse) for p in dto.cv_curve],
            diagnostics=DiagnosticsResponse(mean_residual=dto.diagnostics.mean_residual),
            prediction_formula=dto.prediction_formula,
            n_observations=dto.n_observations,
            interpretation=InterpretationResponse(
                behavior=dto.interpretation.behavior,
                regularization_impact=dto.interpretation.regularization_impact,
                market_change=dto.interpretation.market_change,
                forecast_reliability=dto.interpretation.forecast_reliability,
                limitations=dto.interpretation.limitations,
            ),
        )
