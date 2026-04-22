import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

const intFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

export default function QualityPanel({ result }: Props) {
  const { metrics, split } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">📈 Качество модели (test)</h2>
      <p>
        MSE: <b>{intFmt.format(Math.round(metrics.mse))}</b>
      </p>
      <p>
        RMSE: <b>{intFmt.format(Math.round(metrics.rmse))} руб.</b>
      </p>
      <p>
        MAE: <b>{intFmt.format(Math.round(metrics.mae))} руб.</b>
      </p>
      <p>
        Разделение данных: train={split.train_size}, test={split.test_size}
      </p>
    </div>
  );
}
