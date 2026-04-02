# src/domain/services/model_interpreter.py


from src.domain.models.regression_result import RegressionResult


class ModelInterpreter:

    def _quality_label(self, r2: float) -> str:
        if r2 < 0.5:
            return "слабое"
        if r2 < 0.75:
            return "умеренное"
        if r2 < 0.9:
            return "хорошее"
        return "очень хорошее"

    def _market_shift_text(self, current: float, prior: float | None, entity: str) -> str:
        if prior is None or abs(prior) < 1e-12:
            return f"Для {entity} нет базы сравнения с прошлым периодом."

        delta_pct = ((current - prior) / prior) * 100
        abs_pct = abs(delta_pct)

        if abs_pct < 5:
            trend = "изменилась незначительно"
        elif abs_pct < 15:
            trend = "заметно изменилась"
        else:
            trend = "существенно изменилась"

        direction = "выросла" if delta_pct > 0 else "снизилась"
        return f"Стоимость {entity} {trend}: {direction} на {abs_pct:.1f}% относительно прошлого периода."

    def interpret(self, result: RegressionResult) -> dict:

        metrics = result.metrics
        lb = result.lambda_beta
        la = result.lambda_alpha

        if max(lb, la) > 100:
            behavior = (
                "Новые данные имеют высокий разброс, поэтому модель частично опирается на данные предыдущего периода."
            )
        elif max(lb, la) < 1:
            behavior = (
                "Новые данные стабильны, модель в основном опирается на текущие наблюдения."
            )
        else:
            behavior = (
                "Использован сбалансированный компромисс между текущими и историческими данными."
            )

        house_text = self._market_shift_text(
            current=result.parameters.beta,
            prior=result.beta_prior,
            entity="дома",
        )
        land_text = self._market_shift_text(
            current=result.parameters.alpha,
            prior=result.alpha_prior,
            entity="участка",
        )

        quality_label = self._quality_label(metrics.r2)
        quality = f"Качество модели: {quality_label} (R² = {metrics.r2:.2f})."

        return {
            "behavior": behavior,
            "market_change": f"{house_text} {land_text}",
            "quality": quality,
        }
