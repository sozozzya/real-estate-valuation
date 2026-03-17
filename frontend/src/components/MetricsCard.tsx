//src/components/MetricsCard.tsx

interface Props {
  label: string;
  value: number;
}

export default function MetricsCard({ label, value }: Props) {
  return (
    <div className="metric-item">
      <span className="metric-label">{label}</span>
      <span className="metric-value">
        {value.toLocaleString(undefined, {
          maximumFractionDigits: 4,
        })}
      </span>
    </div>
  );
}
