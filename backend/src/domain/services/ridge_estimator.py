# src/domain/services/ridge_estimator.py


from src.domain.services.matrix_builder import MatrixBuilder
from src.domain.models.regression_data import RegressionData
from src.domain.models.regression_result import RegressionResult
from src.domain.models.ridge_prior import RidgePrior
from src.domain.services.gamma_strategy import GammaStrategy
from src.domain.services.metrics import MetricsCalculator
from src.domain.services.ridge_solver import RidgeSolver


class RidgeEstimator:
    """
    High-level domain service:
    - builds matrices
    - computes gamma
    - solves ridge system
    - calculates metrics
    """

    def __init__(
        self,
        gamma_strategy: GammaStrategy,
        solver: RidgeSolver | None = None,
        matrix_builder: MatrixBuilder | None = None,
        metrics_calculator: MetricsCalculator | None = None,
    ):

        self._gamma_strategy = gamma_strategy
        self._solver = solver or RidgeSolver()
        self._matrix_builder = matrix_builder or MatrixBuilder()
        self._metrics_calculator = metrics_calculator or MetricsCalculator()

    def estimate(
        self,
        data: RegressionData,
        prior: RidgePrior,
    ) -> RegressionResult:

        X, y = self._matrix_builder.build(data)

        gamma = self._gamma_strategy.compute(X, y)

        params = self._solver.solve(X, y, prior, gamma)

        metrics = self._metrics_calculator.calculate(X, y, params)

        return RegressionResult(
            parameters=params,
            metrics=metrics,
            gamma=gamma,
            n_observations=data.size,
        )
