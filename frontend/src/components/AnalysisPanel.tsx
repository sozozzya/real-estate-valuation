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
import type { Property, RegressionParameters } from "../types/apiTypes";

interface Props {
  properties: Property[];
  parameters: RegressionParameters;
}

const moneyFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

const predict = (p: Property, params: RegressionParameters) =>
  params.beta * p.house_area + params.alpha * p.land_area;

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

const fitLine = (xs: number[], ys: number[]) => {
  const n = xs.length;
  if (n < 2) return { slope: 0, intercept: 0 };
  const meanX = xs.reduce((a, b) => a + b, 0) / n;
  const meanY = ys.reduce((a, b) => a + b, 0) / n;

  const num = xs.reduce((sum, x, i) => sum + (x - meanX) * (ys[i] - meanY), 0);
  const den = xs.reduce((sum, x) => sum + (x - meanX) ** 2, 0) || 1;

  const slope = num / den;
  const intercept = meanY - slope * meanX;
  return { slope, intercept };
};

export default function AnalysisPanel({ properties, parameters }: Props) {
  const points = properties.map((p, index) => {
    const predicted = predict(p, parameters);
    return {
      index: index + 1,
      actual: p.price,
      predicted,
      residual: p.price - predicted,
      house_area: p.house_area,
      land_area: p.land_area,
    };
  });

  const minPrice = Math.min(...points.map((p) => Math.min(p.actual, p.predicted)));
  const maxPrice = Math.max(...points.map((p) => Math.max(p.actual, p.predicted)));
  const diag = [
    { x: minPrice, y: minPrice },
    { x: maxPrice, y: maxPrice },
  ];

  const residualHist = buildHistogram(points.map((p) => p.residual));

  const houseFit = fitLine(
    points.map((p) => p.house_area),
    points.map((p) => p.actual),
  );
  const landFit = fitLine(
    points.map((p) => p.land_area),
    points.map((p) => p.actual),
  );

  const houseMin = Math.min(...points.map((p) => p.house_area));
  const houseMax = Math.max(...points.map((p) => p.house_area));
  const landMin = Math.min(...points.map((p) => p.land_area));
  const landMax = Math.max(...points.map((p) => p.land_area));

  return (
    <div className="result-card">
      <h2 className="result-title">📉 Анализ данных и ошибок</h2>

      <h3>Факт vs Прогноз</h3>
      <ResponsiveContainer width="100%" height={320}>
        <ComposedChart data={points}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" dataKey="actual" name="Фактическая цена" unit=" руб." domain={["auto", "auto"]} />
          <YAxis type="number" dataKey="predicted" name="Расчётная цена" unit=" руб." domain={["auto", "auto"]} />
          <Tooltip formatter={(v: number) => `${moneyFmt.format(Math.round(v))} руб.`} />
          <Scatter data={points} fill="#2563eb" />
          <Line data={diag} dataKey="y" type="linear" dot={false} stroke="#ef4444" strokeDasharray="5 5" />
        </ComposedChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: 16 }}>Остатки</h3>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" dataKey="predicted" name="Расчётная цена" unit=" руб." />
          <YAxis type="number" dataKey="residual" name="Ошибка" unit=" руб." />
          <Tooltip formatter={(v: number) => `${moneyFmt.format(Math.round(v))} руб.`} />
          <ReferenceLine y={0} stroke="#ef4444" strokeDasharray="4 4" />
          <Scatter data={points} fill="#16a34a" />
        </ScatterChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: 16 }}>Гистограмма остатков (опционально)</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={residualHist}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="range" interval={0} angle={-20} textAnchor="end" height={70} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#0ea5e9" />
        </BarChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: 16 }}>Цена vs площадь дома</h3>
      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={points}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" dataKey="house_area" unit=" м²" />
          <YAxis type="number" dataKey="actual" unit=" руб." />
          <Tooltip formatter={(v: number) => `${moneyFmt.format(Math.round(v))} руб.`} />
          <Scatter data={points} fill="#6366f1" />
          <Line
            data={[
              { house_area: houseMin, actual: houseFit.slope * houseMin + houseFit.intercept },
              { house_area: houseMax, actual: houseFit.slope * houseMax + houseFit.intercept },
            ]}
            dataKey="actual"
            dot={false}
            stroke="#ef4444"
          />
        </ComposedChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: 16 }}>Цена vs площадь участка</h3>
      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={points}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" dataKey="land_area" unit=" м²" />
          <YAxis type="number" dataKey="actual" unit=" руб." />
          <Tooltip formatter={(v: number) => `${moneyFmt.format(Math.round(v))} руб.`} />
          <Scatter data={points} fill="#f59e0b" />
          <Line
            data={[
              { land_area: landMin, actual: landFit.slope * landMin + landFit.intercept },
              { land_area: landMax, actual: landFit.slope * landMax + landFit.intercept },
            ]}
            dataKey="actual"
            dot={false}
            stroke="#ef4444"
          />
        </ComposedChart>
      </ResponsiveContainer>

      <h3 style={{ marginTop: 16 }}>Таблица фактических и расчётных значений</h3>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>#</th>
              <th>Факт, руб.</th>
              <th>Прогноз, руб.</th>
              <th>Ошибка, руб.</th>
            </tr>
          </thead>
          <tbody>
            {points.map((p) => (
              <tr key={p.index}>
                <td>{p.index}</td>
                <td>{moneyFmt.format(Math.round(p.actual))}</td>
                <td>{moneyFmt.format(Math.round(p.predicted))}</td>
                <td>{moneyFmt.format(Math.round(p.residual))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
