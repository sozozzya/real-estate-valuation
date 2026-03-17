# src/application/services/ridge_application_service.py

import logging

from src.application.factories.gamma_strategy_factory import (
    GammaStrategyFactory,
)
from src.application.mappers.input_mapper import InputMapper
from src.application.mappers.result_mapper import ResultMapper
from src.domain.exceptions import DomainError
from src.domain.services.ridge_estimator import RidgeEstimator

logger = logging.getLogger("ridge_application_service")


class RidgeApplicationService:

    def __init__(self, estimator_factory=None):
        self._estimator_factory = estimator_factory or RidgeEstimator

    def execute(self, input_dto):

        logger.info(
            "ridge_application_service_started",
            extra={
                "n_properties": len(input_dto.properties),
                "auto_gamma": input_dto.auto_gamma,
            },
        )

        try:

            gamma_strategy = GammaStrategyFactory.create(
                auto_gamma=input_dto.auto_gamma,
                gamma=input_dto.gamma,
            )

            data, prior = InputMapper.to_domain(input_dto)

            estimator = self._estimator_factory(
                gamma_strategy=gamma_strategy
            )

            result = estimator.estimate(
                data=data,
                prior=prior,
            )

            output = ResultMapper.to_dto(result)

            logger.info(
                "ridge_application_service_completed",
                extra={
                    "gamma_used": output.gamma_used,
                    "n_observations": output.n_observations,
                },
            )

            return output

        except DomainError:
            logger.warning(
                "ridge_application_service_domain_error",
                exc_info=True,
            )
            raise

        except Exception:
            logger.exception(
                "ridge_application_service_unexpected_error",
            )
            raise
