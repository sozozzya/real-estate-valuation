//src/components/GammaSelector.tsx

interface Props {
  auto: boolean;
  lambdaValue?: number;
  onChange: (auto: boolean, lambdaValue?: number) => void;
}

export default function GammaSelector({
  auto,
  lambdaValue,
  onChange,
}: Props) {
  return (
    <div className="card-block">
      <h2 className="section-title">Регуляризация (λ)</h2>

      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={auto}
          onChange={(e) =>
            onChange(
              e.target.checked,
              e.target.checked ? undefined : lambdaValue,
            )
          }
        />
        Автоматический подбор λ
      </label>

      {!auto && (
        <input
          type="number"
          step="0.001"
          value={lambdaValue ?? ""}
          placeholder="Введите λ"
          className="input"
          onChange={(e) => {
            const value = Number(e.target.value);
            onChange(
              false,
              Number.isFinite(value) ? value : undefined,
            );
          }}
        />
      )}
    </div>
  );
}
