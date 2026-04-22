# src/presentation/api/routes.py

import logging
import anyio
from fastapi import APIRouter, Depends, HTTPException, status

from src.presentation.api.dependencies import get_calculate_use_case
from src.presentation.api.mappers import RequestMapper, ResponseMapper
from src.presentation.api.schemas import CalculateRequest, CalculateResponse
from src.domain.exceptions import DomainError
from src.application.use_cases.calculate_ridge_use_case import CalculateRidgeUseCase

logger = logging.getLogger("api.routes")

router = APIRouter()


@router.post("/calculate", response_model=CalculateResponse)
async def calculate(
    request: CalculateRequest,
    use_case: CalculateRidgeUseCase = Depends(get_calculate_use_case),
):
    logger.info(
        "calculate_request_received",
        extra={
            "n_properties": len(request.properties),
            "auto_lambda": request.auto_lambda,
        },
    )

    try:

        dto = RequestMapper.to_dto(request)

        result = await anyio.to_thread.run_sync(
            use_case.execute,
            dto,
        )

        response = ResponseMapper.from_dto(result)

        logger.info(
            "calculate_request_completed",
            extra={
                "lambda_star": response.lambda_star,
                "n_observations": response.n_observations,
                "test_mse": response.metrics.mse,
            },
        )

        return response

    except DomainError as e:

        logger.warning(
            "calculate_request_domain_error",
            exc_info=True,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception:

        logger.exception(
            "calculate_request_unexpected_error",
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
