//src/components/PriceChart.tsx

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface ChartPoint {
  index: number;
  actual: number;
  predicted: number;
}

interface Props {
  data: ChartPoint[];
}

export default function PriceChart({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="index" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="actual"
          stroke="#2563eb"
          name="Фактическая цена"
        />
        <Line
          type="monotone"
          dataKey="predicted"
          stroke="#16a34a"
          name="Прогноз"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
