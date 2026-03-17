from src.application.dto.calculate_input import CalculateRidgeInputDTO
from src.application.dto.calculate_result import CalculateRidgeResultDTO
from src.application.validators.calculate_validator import CalculateValidator
from src.application.services.ridge_application_service import RidgeApplicationService


class CalculateRidgeUseCase:

    def __init__(
        self,
        validator: CalculateValidator,
        service: RidgeApplicationService,
    ):
        self.validator = validator
        self.service = service

    def execute(self, dto: CalculateRidgeInputDTO) -> CalculateRidgeResultDTO:

        # validation
        self.validator.validate(dto)

        # delegate to application service
        return self.service.execute(dto)
