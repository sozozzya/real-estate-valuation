# src/domain/services/gamma_strategy.py

import numpy as np
from abc import ABC, abstractmethod

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
    """
    Automatically selects gamma based on data variance.
    Useful when dataset is small and noisy.
    """

    def __init__(self, scale: float = 0.01):
        if scale <= 0:
            raise GammaStrategyError("scale must be positive.")
        self._scale = scale

    def compute(self, X: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        try:
            variance_y = np.var(y)
            variance_s = np.var(X[:, 0])
            variance_q = np.var(X[:, 1])

            lambda_beta = self._scale * variance_y / max(variance_s, 1e-8)
            lambda_alpha = self._scale * variance_y / max(variance_q, 1e-8)

            return float(lambda_beta), float(lambda_alpha)
        except Exception as e:
            raise GammaStrategyError("failed to compute lambdas") from e
