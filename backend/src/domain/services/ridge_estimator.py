# src/domain/services/ridge_estimator.py


from src.domain.services.matrix_builder import MatrixBuilder
from src.domain.models.regression_data import RegressionData
from src.domain.models.regression_result import RegressionResult
from src.domain.models.ridge_prior import RidgePrior
from src.domain.services.gamma_strategy import GammaStrategy
from src.domain.services.metrics import MetricsCalculator
from src.domain.services.ridge_solver import RidgeSolver
from src.domain.services.uncertainty_estimator import UncertaintyEstimator


class RidgeEstimator:
    """
    High-level domain service:
    - builds matrices
    - computes lambdas
    - solves targeted ridge system
    - calculates metrics and uncertainty
    """

    def __init__(
        self,
        gamma_strategy: GammaStrategy,
        solver: RidgeSolver | None = None,
        matrix_builder: MatrixBuilder | None = None,
        metrics_calculator: MetricsCalculator | None = None,
        uncertainty_estimator: UncertaintyEstimator | None = None,
    ):

        self._gamma_strategy = gamma_strategy
        self._solver = solver or RidgeSolver()
        self._matrix_builder = matrix_builder or MatrixBuilder()
        self._metrics_calculator = metrics_calculator or MetricsCalculator()
        self._uncertainty_estimator = uncertainty_estimator or UncertaintyEstimator()

    def estimate(
        self,
        data: RegressionData,
        prior: RidgePrior,
    ) -> RegressionResult:

        X, y = self._matrix_builder.build(data)

        lambda_beta, lambda_alpha = self._gamma_strategy.compute(X, y)

        params = self._solver.solve(
            X,
            y,
            prior,
            lambda_beta=lambda_beta,
            lambda_alpha=lambda_alpha,
        )

        metrics = self._metrics_calculator.calculate(X, y, params)
        uncertainty = self._uncertainty_estimator.estimate(
            X=X,
            y=y,
            params=params,
            lambda_beta=lambda_beta,
            lambda_alpha=lambda_alpha,
        )

        return RegressionResult(
            parameters=params,
            metrics=metrics,
<<<<<<< HEAD
            uncertainty=uncertainty,
            lambda_beta=lambda_beta,
            lambda_alpha=lambda_alpha,
            prediction_formula=f"V = {params.beta:.4f} * S + {params.alpha:.4f} * Q",
=======
            lambda_beta=lambda_beta,
            lambda_alpha=lambda_alpha,
>>>>>>> main
            n_observations=data.size,
        )
