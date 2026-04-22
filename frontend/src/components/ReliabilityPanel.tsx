import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

const intFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

export default function ReliabilityPanel({ result }: Props) {
  const { uncertainty } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">📊 Надёжность и устойчивость параметров</h2>
      <p>
        95% доверительный интервал для дома: <b>{intFmt.format(Math.round(uncertainty.beta_ci_95.lower))} – {intFmt.format(Math.round(uncertainty.beta_ci_95.upper))} руб./м²</b>
      </p>
      <p>
        95% доверительный интервал для участка: <b>{intFmt.format(Math.round(uncertainty.alpha_ci_95.lower))} – {intFmt.format(Math.round(uncertainty.alpha_ci_95.upper))} руб./м²</b>
      </p>
      <p>
        Изменение относительно предыдущего периода: дом <b>{uncertainty.beta_shift_pct.toFixed(1)}%</b>, участок <b>{uncertainty.alpha_shift_pct.toFixed(1)}%</b>
      </p>
      <p>
        Сила регуляризации: <b>{uncertainty.regularization_strength}</b>
      </p>
    </div>
  );
}
