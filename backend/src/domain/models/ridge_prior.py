# src/domain/models/ridge_prior.py

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass(frozen=True)
class RidgePrior:

    beta_prior: Optional[float]
    alpha_prior: Optional[float]

    def as_vector(self) -> np.ndarray:

        beta = 0.0 if self.beta_prior is None else self.beta_prior
        alpha = 0.0 if self.alpha_prior is None else self.alpha_prior

        return np.array(
            [beta, alpha],
            dtype=float
        )
