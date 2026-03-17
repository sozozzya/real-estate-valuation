// src/components/InterpretationPanel.tsx

import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

export default function InterpretationPanel({ result }: Props) {
  const { parameters, gamma_used, interpretation } = result;

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
        Использованный коэффициент регуляризации γ ={" "}
        <b>{gamma_used.toFixed(2)}</b>
      </p>

      <p className="mt-2">
        <b>{interpretation.summary}</b>
      </p>

      <p>Качество модели: {interpretation.quality}</p>
    </div>
  );
}
