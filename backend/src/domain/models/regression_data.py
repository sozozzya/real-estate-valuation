# src/domain/models/regression_data.py


from dataclasses import dataclass
from typing import Sequence

from src.domain.exceptions import ValidationError
from src.domain.models.property import Property


@dataclass(frozen=True)
class RegressionData:
    properties: Sequence[Property]

    def __post_init__(self):

        if len(self.properties) < 2:
            raise ValidationError(
                f"at least two observations required, got {len(self.properties)}"
            )

    @property
    def size(self) -> int:
        return len(self.properties)
