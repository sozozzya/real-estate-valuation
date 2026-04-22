import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Line,
  ComposedChart,
  BarChart,
  Bar,
} from "recharts";
import type { CalculateResponse, Property } from "../types/apiTypes";

interface Props {
  properties: Property[];
  result: CalculateResponse;
}

const moneyFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

const predict = (p: Property, beta: number, alpha: number) => beta * p.house_area + alpha * p.land_area;

const buildHistogram = (values: number[], bins = 8) => {
  if (values.length === 0) return [];
  const min = Math.min(...values);
  const max = Math.max(...values);
  const width = Math.max((max - min) / bins, 1);
  const hist = Array.from({ length: bins }, (_, i) => ({
    range: `${moneyFmt.format(Math.round(min + i * width))}…${moneyFmt.format(Math.round(min + (i + 1) * width))}`,
    count: 0,
  }));
  values.forEach((v) => {
    const idx = Math.min(Math.floor((v - min) / width), bins - 1);
    hist[idx].count += 1;
  });
  return hist;
};

export default function AnalysisPanel({ properties, result }: Props) {
  const { parameters, metrics, diagnostics } = result;

  const points = properties.map((p) => {
    const predicted = predict(p, parameters.beta, parameters.alpha);
    return {
      actual: p.price,
      predicted,
      residual: p.price - predicted,
      house_area: p.house_area,
      land_area: p.land_area,
    };
  });

  const minPrice = Math.min(...points.map((p) => Math.min(p.actual, p.predicted)));
  const maxPrice = Math.max(...points.map((p) => Math.max(p.actual, p.predicted)));
  const diag = [{ x: minPrice, y: minPrice }, { x: maxPrice, y: maxPrice }];
  const residualHist = buildHistogram(points.map((p) => p.residual));

  return (
    <div className="result-card">
      <h2 className="result-title">📉 Диагностика модели (графики)</h2>

      <h3>Факт vs Прогноз</h3>
      <p>R² (LOOCV) = {metrics.r2_loocv.toFixed(2)}; RMSE (LOOCV) = {moneyFmt.format(Math.round(metrics.rmse_loocv))} руб.</p>
      <ResponsiveContainer width="100%" height={320}>
        <ComposedChart data={points}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" dataKey="actual" unit=" руб." label={{ value: "Фактическая цена, руб.", position: "insideBottom", offset: -5 }} />
          <YAxis type="number" dataKey="predicted" unit=" руб." label={{ value: "Расчётная цена, руб.", angle: -90, position: "insideLeft" }} />
          <Tooltip formatter={(v: number) => `${moneyFmt.format(Math.round(v))} руб.`} />
          <Scatter data={points} fill="#2563eb" />
          <Line data={diag} dataKey="y" type="linear" dot={false} stroke="#ef4444" strokeDasharray="5 5" />
        </ComposedChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: 16 }}>Остатки</h3>
      <p>Среднее значение остатка: {moneyFmt.format(Math.round(diagnostics.mean_residual))} руб.</p>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" dataKey="predicted" unit=" руб." label={{ value: "Расчётная цена, руб.", position: "insideBottom", offset: -5 }} />
          <YAxis type="number" dataKey="residual" unit=" руб." label={{ value: "Ошибка (остаток), руб.", angle: -90, position: "insideLeft" }} />
          <Tooltip formatter={(v: number) => `${moneyFmt.format(Math.round(v))} руб.`} />
          <ReferenceLine y={0} stroke="#ef4444" strokeDasharray="4 4" />
          <Scatter data={points} fill="#16a34a" />
        </ScatterChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: 16 }}>Гистограмма остатков (опционально)</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={residualHist}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="range" interval={0} angle={-20} textAnchor="end" height={70} label={{ value: "Ошибка, руб.", position: "insideBottom", offset: -5 }} />
          <YAxis label={{ value: "Частота", angle: -90, position: "insideLeft" }} />
          <Tooltip />
          <Bar dataKey="count" fill="#0ea5e9" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
