// src/components/ResultsPanel.tsx

import type { CalculateResponse } from "../types/apiTypes";
import MetricsCard from "./MetricsCard";

interface Props {
  result: CalculateResponse;
}

export default function ResultsPanel({ result }: Props) {
  const { parameters, metrics, lambda_beta_used, lambda_alpha_used } = result;

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
        <MetricsCard label="λβ" value={lambda_beta_used} />
        <MetricsCard label="λα" value={lambda_alpha_used} />
      </div>
    </div>
  );
}
