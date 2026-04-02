# src/domain/models/ridge_parameters.py

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RidgeParameters:

    beta: float
    alpha: float

    def as_vector(self) -> np.ndarray:

        return np.array(
            [self.beta, self.alpha],
            dtype=float
        )
