# src/domain/services/model_interpreter.py


from src.domain.models.regression_result import RegressionResult


class ModelInterpreter:

    def interpret(self, result: RegressionResult) -> dict:

        metrics = result.metrics
        lb = result.lambda_beta
        la = result.lambda_alpha

        if max(lb, la) > 100:
            regularization_comment = (
                "Новые данные шумные: модель сильнее опирается на априорные оценки."
            )
        elif max(lb, la) < 1:
            regularization_comment = (
                "Новые данные информативны: оценки в основном определяются текущей выборкой."
            )
        else:
            regularization_comment = (
                "Использован сбалансированный компромисс между историей и текущими данными."
            )

        return {
            "summary": regularization_comment,
            "model_quality": "Good fit" if metrics.r2 > 0.7 else "Weak fit",
        }
