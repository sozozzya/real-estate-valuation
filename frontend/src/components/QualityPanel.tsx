import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

const intFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

const qualityLabel = (r2: number): string => {
  if (r2 < 0.5) return "слабое";
  if (r2 < 0.75) return "умеренное";
  if (r2 < 0.9) return "хорошее";
  return "очень хорошее";
};

export default function QualityPanel({ result }: Props) {
  const { metrics } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">📈 Качество и обобщающая способность (LOOCV)</h2>
      <p>
        R² (LOOCV): <b>{metrics.r2_loocv.toFixed(2)} — {qualityLabel(metrics.r2_loocv)}</b>
      </p>
      <p>
        RMSE (LOOCV): <b>{intFmt.format(Math.round(metrics.rmse_loocv))} руб.</b>
      </p>
      <p>
        MAE (LOOCV): <b>{intFmt.format(Math.round(metrics.mae_loocv))} руб.</b>
      </p>
      <p>
        MAPE (LOOCV): <b>{metrics.mape_loocv.toFixed(1)}%</b>
      </p>
    </div>
  );
}
