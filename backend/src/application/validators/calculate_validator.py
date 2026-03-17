# src/application/validators/calculate_validator.py


from src.application.dto.calculate_input import CalculateRidgeInputDTO
from src.domain.exceptions import ValidationError


class CalculateValidator:

    def validate(self, dto: CalculateRidgeInputDTO) -> None:

        properties = dto.properties

        if not properties:
            raise ValidationError("property list cannot be empty")

        if len(properties) < 2:
            raise ValidationError(
                f"at least two observations required, got {len(properties)}"
            )

        for i, p in enumerate(properties):

            if p.price <= 0:
                raise ValidationError(
                    f"price must be positive at index {i}"
                )

            if p.house_area <= 0:
                raise ValidationError(
                    f"house_area must be positive at index {i}"
                )

            if p.land_area <= 0:
                raise ValidationError(
                    f"land_area must be positive at index {i}"
                )

        if not dto.auto_gamma:

            if dto.gamma is None:
                raise ValidationError(
                    "gamma must be provided when auto_gamma is False"
                )

            if dto.gamma < 0:
                raise ValidationError(
                    f"gamma must be non-negative, got {dto.gamma}"
                )
