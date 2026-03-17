// src/components/ResultsPanel.tsx

import type { CalculateResponse } from "../types/apiTypes";
import MetricsCard from "./MetricsCard";

interface Props {
  result: CalculateResponse;
}

export default function ResultsPanel({ result }: Props) {
  const { parameters, metrics, gamma_used } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">Результаты оценки</h2>

      <div className="metrics-grid">
        <MetricsCard label="β — дом" value={parameters.beta} />
        <MetricsCard label="α — участок" value={parameters.alpha} />
        <MetricsCard label="Свободный член" value={parameters.intercept} />

        <MetricsCard label="R²" value={metrics.r2} />
        <MetricsCard label="RMSE" value={metrics.rmse} />
        <MetricsCard label="MAE" value={metrics.mae} />
        <MetricsCard label="γ" value={gamma_used} />
      </div>
    </div>
  );
}
