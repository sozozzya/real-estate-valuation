# src/domain/services/gamma_strategy.py

import numpy as np
from abc import ABC, abstractmethod

from src.domain.exceptions import GammaStrategyError


class GammaStrategy(ABC):
    """Abstract gamma selection strategy."""

    @abstractmethod
    def compute(self, X: np.ndarray, y: np.ndarray) -> float:
        pass


class FixedGammaStrategy(GammaStrategy):
    """User-defined constant gamma."""

    def __init__(self, gamma: float):
        if gamma < 0:
            raise GammaStrategyError("gamma must be non-negative.")
        self._gamma = gamma

    def compute(self, X: np.ndarray, y: np.ndarray) -> float:
        return self._gamma


class VarianceBasedGammaStrategy(GammaStrategy):
    """
    Automatically selects gamma based on data variance.
    Useful when dataset is small and noisy.
    """

    def __init__(self, scale: float = 0.01):
        if scale <= 0:
            raise GammaStrategyError("scale must be positive.")
        self._scale = scale

    def compute(self, X: np.ndarray, y: np.ndarray) -> float:
        try:
            variance = np.var(y)
            gamma = self._scale * variance
            return float(gamma)
        except Exception as e:
            raise GammaStrategyError("failed to compute gamma") from e
