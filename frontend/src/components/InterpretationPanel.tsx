// src/components/InterpretationPanel.tsx

import { useMemo, useState } from "react";
import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

const intFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

export default function InterpretationPanel({ result }: Props) {
  const { parameters, lambda_beta_used, lambda_alpha_used, uncertainty, interpretation } = result;

  const [houseArea, setHouseArea] = useState<number | undefined>();
  const [landArea, setLandArea] = useState<number | undefined>();
  const [advanced, setAdvanced] = useState(false);

  const estimatedPrice = useMemo(() => {
    if (!houseArea || !landArea || houseArea <= 0 || landArea <= 0) return undefined;
    return parameters.beta * houseArea + parameters.alpha * landArea;
  }, [houseArea, landArea, parameters.alpha, parameters.beta]);

  return (
    <div className="bg-white p-4 rounded shadow mt-6">
      <h3 className="font-semibold mb-2">📊 Надёжность оценок</h3>

      <p>
        95% доверительный интервал для дома: <b>{intFmt.format(Math.round(uncertainty.beta_ci_95.lower))} – {intFmt.format(Math.round(uncertainty.beta_ci_95.upper))} €/м²</b>
      </p>
      <p>
        95% доверительный интервал для участка: <b>{intFmt.format(Math.round(uncertainty.alpha_ci_95.lower))} – {intFmt.format(Math.round(uncertainty.alpha_ci_95.upper))} €/м²</b>
      </p>

      <h3 className="font-semibold mt-4 mb-2">🏷 Оценка конкретного объекта</h3>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, maxWidth: 480 }}>
        <input
          className="input"
          type="number"
          placeholder="Площадь дома S"
          value={houseArea ?? ""}
          onChange={(e) => setHouseArea(Number(e.target.value) || undefined)}
        />
        <input
          className="input"
          type="number"
          placeholder="Площадь участка Q"
          value={landArea ?? ""}
          onChange={(e) => setLandArea(Number(e.target.value) || undefined)}
        />
      </div>
      {estimatedPrice !== undefined && (
        <p style={{ marginTop: 8 }}>
          Оценка стоимости объекта: <b>{intFmt.format(Math.round(estimatedPrice))} €</b>
        </p>
      )}

      <h3 className="font-semibold mt-4 mb-2">🧠 Интерпретация</h3>
      <p>{interpretation.behavior}</p>
      <p>{interpretation.market_change}</p>
      <p><b>{interpretation.quality}</b></p>

      <label style={{ display: "block", marginTop: 12 }}>
        <input type="checkbox" checked={advanced} onChange={(e) => setAdvanced(e.target.checked)} />{" "}
        Показать расширенную статистику
      </label>

      {advanced && (
        <div style={{ marginTop: 8 }}>
          <p>SE(β): {uncertainty.beta_standard_error.toFixed(2)}</p>
          <p>SE(α): {uncertainty.alpha_standard_error.toFixed(2)}</p>
          <p>Сила регуляризации (дом): {lambda_beta_used.toFixed(2)}</p>
          <p>Сила регуляризации (участок): {lambda_alpha_used.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
}
