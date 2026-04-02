import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

const intFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });
const pctFmt = new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

export default function QualityPanel({ result }: Props) {
  const { metrics, interpretation } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">📈 Качество модели</h2>
      <p><b>{interpretation.quality}</b></p>
      <p>
        Средняя ошибка: <b>{intFmt.format(Math.round(metrics.rmse))} руб.</b>
      </p>
      <p>
        Средняя ошибка (MAPE): <b>{pctFmt.format(metrics.mape)}%</b>
      </p>
    </div>
  );
}
