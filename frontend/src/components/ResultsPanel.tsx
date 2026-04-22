// src/components/ResultsPanel.tsx

import { useMemo, useState } from "react";
import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
}

const intFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

const formatUnitPrice = (value: number): string => {
  if (Math.abs(value) >= 100) {
    return intFmt.format(Math.round(value));
  }
  return new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2 }).format(value);
};

export default function ResultsPanel({ result }: Props) {
  const { parameters } = result;
  const [houseArea, setHouseArea] = useState<number | undefined>();
  const [landArea, setLandArea] = useState<number | undefined>();

  const estimatedPrice = useMemo(() => {
    if (!houseArea || !landArea || houseArea <= 0 || landArea <= 0) return undefined;
    return parameters.beta * houseArea + parameters.alpha * landArea;
  }, [houseArea, landArea, parameters.alpha, parameters.beta]);

  return (
    <div className="result-card">
      <h2 className="result-title">🧾 Результат модели</h2>
      <p>Модель оценки (регуляризованная регрессия с учётом предыдущего периода)</p>

      <p>
        Удельная стоимость дома: <b>{formatUnitPrice(parameters.beta)} руб./м²</b>
      </p>
      <p>
        Удельная стоимость участка: <b>{formatUnitPrice(parameters.alpha)} руб./м²</b>
      </p>

      <p style={{ marginTop: 12 }}>
        Модель оценки: <b>V = {formatUnitPrice(parameters.beta)} × S + {formatUnitPrice(parameters.alpha)} × Q</b>
      </p>

      <h3 style={{ marginTop: 16 }}>Оценка стоимости объекта</h3>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, maxWidth: 480 }}>
        <input
          className="input"
          type="number"
          placeholder="Площадь дома S, м²"
          value={houseArea ?? ""}
          onChange={(e) => setHouseArea(Number(e.target.value) || undefined)}
        />
        <input
          className="input"
          type="number"
          placeholder="Площадь участка Q, м²"
          value={landArea ?? ""}
          onChange={(e) => setLandArea(Number(e.target.value) || undefined)}
        />
      </div>

      {estimatedPrice !== undefined && (
        <p>
          Оценка стоимости объекта: <b>{intFmt.format(Math.round(estimatedPrice))} руб.</b>
        </p>
      )}
    </div>
  );
}
