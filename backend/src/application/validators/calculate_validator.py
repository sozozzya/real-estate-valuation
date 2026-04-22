from src.application.dto.calculate_input import CalculateRidgeInputDTO
from src.domain.exceptions import ValidationError


class CalculateValidator:

    def validate(self, dto: CalculateRidgeInputDTO) -> None:

        properties = dto.properties

        if not properties:
            raise ValidationError("property list cannot be empty")

        if len(properties) < 5:
            raise ValidationError(
                f"at least five observations required for train/test + LOOCV, got {len(properties)}"
            )

        for i, p in enumerate(properties):
            if p.price <= 0:
                raise ValidationError(f"price must be positive at index {i}")
            if p.house_area <= 0:
                raise ValidationError(f"house_area must be positive at index {i}")
            if p.land_area <= 0:
                raise ValidationError(f"land_area must be positive at index {i}")

        if not dto.auto_lambda:
            if dto.lambda_beta is None or dto.lambda_alpha is None:
                raise ValidationError("lambda_beta and lambda_alpha must be provided when auto_lambda is False")
            if dto.lambda_beta <= 0 or dto.lambda_alpha <= 0:
                raise ValidationError("manual lambda values must be positive")
