# src/domain/services/ridge_solver.py

import numpy as np

from src.domain.exceptions import SingularMatrixError
from src.domain.models.ridge_parameters import RidgeParameters
from src.domain.models.ridge_prior import RidgePrior


class RidgeSolver:
    """
    Solves ridge regression system:

    (XᵀX + Λ)θ = Xᵀy + Λθ₀
    """

    def solve(
        self,
        X: np.ndarray,
        y: np.ndarray,
        prior: RidgePrior,
        lambda_beta: float,
        lambda_alpha: float,
    ) -> RidgeParameters:

        theta0 = prior.as_vector()

        if theta0.shape[0] != X.shape[1]:
            raise ValueError(
                "prior dimension does not match number of model parameters"
            )

        try:

            lambda_matrix = np.diag([lambda_beta, lambda_alpha, 0.0])

            A = X.T @ X + lambda_matrix
            b = X.T @ y + lambda_matrix @ theta0

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
