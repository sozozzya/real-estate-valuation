# src/infrastructure/di/container


from src.application.services.ridge_application_service import (
    RidgeApplicationService,
)
from src.application.use_cases.calculate_ridge_use_case import (
    CalculateRidgeUseCase,
)
from src.application.validators.calculate_validator import CalculateValidator
from src.infrastructure.reporting.excel_report_generator import (
    ExcelReportGenerator,
)


class Container:

    def __init__(self):

        self.validator = CalculateValidator()
        self.service = RidgeApplicationService()
        self.use_case = CalculateRidgeUseCase(
            validator=self.validator, service=self.service
        )

        self.report_generator = ExcelReportGenerator()


container = Container()
