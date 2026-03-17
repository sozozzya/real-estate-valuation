# src/domain/services/model_interpreter.py


from src.domain.models.regression_result import RegressionResult


class ModelInterpreter:

    def interpret(self, result: RegressionResult) -> dict:

        params = result.parameters
        metrics = result.metrics

        return {
            "house_unit_price_comment": f"Estimated house unit price: {params.beta:.2f}",
            "land_unit_price_comment": f"Estimated land unit price: {params.alpha:.2f}",
            "model_quality": "Good fit" if metrics.r2 > 0.7 else "Weak fit",
        }
