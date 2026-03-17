# src/domain/models/property.py


from dataclasses import dataclass

from src.domain.exceptions import ValidationError


@dataclass(frozen=True)
class Property:
    """
    Represents a single real estate object.

    V = βS + αQ + c + ε
    """

    price: float
    house_area: float
    land_area: float

    def __post_init__(self):

        if self.price <= 0:
            raise ValidationError(f"price must be positive, got {self.price}")

        if self.house_area <= 0:
            raise ValidationError(
                f"house_area must be positive, got {self.house_area}"
            )

        if self.land_area <= 0:
            raise ValidationError(
                f"land_area must be positive, got {self.land_area}"
            )
