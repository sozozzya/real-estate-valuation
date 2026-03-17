//src/components/GammaSelector.tsx

interface Props {
  auto: boolean;
  lambdaBeta?: number;
  lambdaAlpha?: number;
  onChange: (auto: boolean, lambdaBeta?: number, lambdaAlpha?: number) => void;
}

export default function GammaSelector({
  auto,
  lambdaBeta,
  lambdaAlpha,
  onChange,
}: Props) {
  return (
    <div className="card-block">
      <h2 className="section-title">Регуляризация (λβ и λα)</h2>

      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={auto}
          onChange={(e) =>
            onChange(
              e.target.checked,
              e.target.checked ? undefined : lambdaBeta,
              e.target.checked ? undefined : lambdaAlpha,
            )
          }
        />
        Автоматический подбор λβ и λα
      </label>

      {!auto && (
        <>
          <input
            type="number"
            step="0.001"
            value={lambdaBeta ?? ""}
            placeholder="Введите λβ"
            className="input"
            onChange={(e) => {
              const value = Number(e.target.value);
              onChange(
                false,
                Number.isFinite(value) ? value : undefined,
                lambdaAlpha,
              );
            }}
          />

          <input
            type="number"
            step="0.001"
            value={lambdaAlpha ?? ""}
            placeholder="Введите λα"
            className="input"
            onChange={(e) => {
              const value = Number(e.target.value);
              onChange(
                false,
                lambdaBeta,
                Number.isFinite(value) ? value : undefined,
              );
            }}
          />
        </>
      )}
    </div>
  );
}
