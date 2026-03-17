# src/domain/services/ridge_solver.py

import numpy as np

from src.domain.exceptions import SingularMatrixError
from src.domain.models.ridge_parameters import RidgeParameters
from src.domain.models.ridge_prior import RidgePrior


class RidgeSolver:
    """
    Solves ridge regression system:

    (XᵀX + γI)θ = Xᵀy + γθ₀
    """

    def solve(
        self,
        X: np.ndarray,
        y: np.ndarray,
        prior: RidgePrior,
        gamma: float,
    ) -> RidgeParameters:

        theta0 = prior.as_vector()

        if theta0.shape[0] != X.shape[1]:
            raise ValueError(
                "prior dimension does not match number of model parameters"
            )

        try:

            identity = np.eye(X.shape[1])
            identity[-1, -1] = 0.0  # intercept not regularized

            A = X.T @ X + gamma * identity
            b = X.T @ y + gamma * theta0

            theta = np.linalg.solve(A, b)

        except np.linalg.LinAlgError as e:
            raise SingularMatrixError(
                "ridge system is singular or ill-conditioned"
            ) from e

        return RidgeParameters(
            beta=float(theta[0]),
            alpha=float(theta[1]),
            intercept=float(theta[2]),
        )
