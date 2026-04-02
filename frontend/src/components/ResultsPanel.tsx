// src/components/ResultsPanel.tsx

import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

const intFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });
const pctFmt = new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

const formatUnitPrice = (value: number): string => {
  if (Math.abs(value) >= 100) {
    return intFmt.format(Math.round(value));
  }
  return new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2 }).format(value);
};

export default function ResultsPanel({ result }: Props) {
  const { parameters, metrics } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">🧾 Результаты оценки</h2>

      <p>
        Удельная стоимость дома: <b>{formatUnitPrice(parameters.beta)} €/м²</b>
      </p>
      <p>
        Удельная стоимость участка: <b>{formatUnitPrice(parameters.alpha)} €/м²</b>
      </p>

      <p style={{ marginTop: 12 }}>
        Модель: <b>V = {formatUnitPrice(parameters.beta)} × S + {formatUnitPrice(parameters.alpha)} × Q</b>
      </p>

      <h3 style={{ marginTop: 16 }}>📈 Качество модели</h3>
      <p>
        R²: <b>{metrics.r2.toFixed(2)}</b>
      </p>
      <p>
        Средняя ошибка (RMSE): <b>{intFmt.format(Math.round(metrics.rmse))} €</b>
      </p>
      <p>
        Средняя ошибка (MAPE): <b>{pctFmt.format(metrics.mape)}%</b>
      </p>
    </div>
  );
}
