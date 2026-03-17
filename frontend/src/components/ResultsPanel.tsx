// src/components/ResultsPanel.tsx

import type { CalculateResponse } from "../types/apiTypes";
import MetricsCard from "./MetricsCard";

interface Props {
  result: CalculateResponse;
}

export default function ResultsPanel({ result }: Props) {
  const { parameters, metrics, uncertainty, lambda_beta_used, lambda_alpha_used } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">Результаты оценки</h2>

      <div className="metrics-grid">
        <MetricsCard label="β — дом" value={parameters.beta} />
        <MetricsCard label="α — участок" value={parameters.alpha} />
        <MetricsCard label="SE(β)" value={uncertainty.beta_standard_error} />
        <MetricsCard label="SE(α)" value={uncertainty.alpha_standard_error} />

        <MetricsCard label="R²" value={metrics.r2} />
        <MetricsCard label="RSS" value={metrics.rss} />
        <MetricsCard label="RMSE" value={metrics.rmse} />
        <MetricsCard label="MAPE, %" value={metrics.mape} />
        <MetricsCard label="λβ" value={lambda_beta_used} />
        <MetricsCard label="λα" value={lambda_alpha_used} />
      </div>
    </div>
  );
}
