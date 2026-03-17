// src/components/InterpretationPanel.tsx

import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

export default function InterpretationPanel({ result }: Props) {
  const { parameters, lambda_beta_used, lambda_alpha_used, prediction_formula, uncertainty, interpretation } = result;

  return (
    <div className="bg-white p-4 rounded shadow mt-6">
      <h3 className="font-semibold mb-2">Интерпретация</h3>

      <p>
        Удельная стоимость дома: <b>{parameters.beta.toFixed(2)}</b>
      </p>

      <p>
        Удельная стоимость участка: <b>{parameters.alpha.toFixed(2)}</b>
      </p>

      <p>
        95% ДИ для β: <b>[{uncertainty.beta_ci_95.lower.toFixed(2)}; {uncertainty.beta_ci_95.upper.toFixed(2)}]</b>
      </p>

      <p>
        95% ДИ для α: <b>[{uncertainty.alpha_ci_95.lower.toFixed(2)}; {uncertainty.alpha_ci_95.upper.toFixed(2)}]</b>
      </p>

      <p>
        Использованные коэффициенты регуляризации λβ и λα ={" "}
        <b>{lambda_beta_used.toFixed(2)} / {lambda_alpha_used.toFixed(2)}</b>
      </p>

      <p>
        Формула прогноза: <b>{prediction_formula}</b>
      </p>

      <p className="mt-2">
        <b>{interpretation.summary}</b>
      </p>

      <p>Качество модели: {interpretation.quality}</p>
    </div>
  );
}
