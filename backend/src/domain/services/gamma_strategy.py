# src/domain/services/gamma_strategy.py

from abc import ABC, abstractmethod

import numpy as np

from src.domain.exceptions import GammaStrategyError


class GammaStrategy(ABC):
    """Abstract regularization selection strategy."""

    @abstractmethod
    def compute(self, X: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        pass


class FixedGammaStrategy(GammaStrategy):
    """User-defined constants for β and α regularization."""

    def __init__(self, lambda_beta: float, lambda_alpha: float):
        if lambda_beta < 0 or lambda_alpha < 0:
            raise GammaStrategyError("lambda values must be non-negative.")
        self._lambda_beta = lambda_beta
        self._lambda_alpha = lambda_alpha

    def compute(self, X: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        return self._lambda_beta, self._lambda_alpha


class VarianceBasedGammaStrategy(GammaStrategy):
    """Automatic λβ and λα tuning using a small LOOCV grid."""

    def __init__(self, scale: float = 1.0):
        if scale <= 0:
            raise GammaStrategyError("scale must be positive.")
        self._scale = scale

<<<<<<< HEAD
    def _fit_theta(
        self,
        X: np.ndarray,
        y: np.ndarray,
        lambda_beta: float,
        lambda_alpha: float,
    ) -> np.ndarray:
        lambda_matrix = np.diag([lambda_beta, lambda_alpha])
        return np.linalg.solve(X.T @ X + lambda_matrix, X.T @ y)

    def compute(self, X: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        try:
            variance_y = max(float(np.var(y)), 1e-8)
            variance_s = max(float(np.var(X[:, 0])), 1e-8)
            variance_q = max(float(np.var(X[:, 1])), 1e-8)

            base_beta = self._scale * variance_y / variance_s
            base_alpha = self._scale * variance_y / variance_q

            multipliers = [0.05, 0.2, 1.0, 5.0, 20.0]
            candidates = [
                (base_beta * mb, base_alpha * ma)
                for mb in multipliers
                for ma in multipliers
            ]

            best = candidates[0]
            best_mse = float("inf")

            n = X.shape[0]
            for lambda_beta, lambda_alpha in candidates:
                sq_errors = []
                for i in range(n):
                    mask = np.ones(n, dtype=bool)
                    mask[i] = False
                    x_train = X[mask]
                    y_train = y[mask]
                    theta = self._fit_theta(x_train, y_train, lambda_beta, lambda_alpha)
                    y_hat = float(X[i] @ theta)
                    sq_errors.append((float(y[i]) - y_hat) ** 2)

                mse = float(np.mean(sq_errors))
                if mse < best_mse:
                    best_mse = mse
                    best = (float(lambda_beta), float(lambda_alpha))

            return best
=======
    def compute(self, X: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        try:
            variance_y = np.var(y)
            variance_s = np.var(X[:, 0])
            variance_q = np.var(X[:, 1])

            lambda_beta = self._scale * variance_y / max(variance_s, 1e-8)
            lambda_alpha = self._scale * variance_y / max(variance_q, 1e-8)

            return float(lambda_beta), float(lambda_alpha)
>>>>>>> main
        except Exception as e:
            raise GammaStrategyError("failed to compute lambdas") from e
