//src/components/GammaSelector.tsx

interface Props {
  auto: boolean;
  gamma?: number;
  onChange: (auto: boolean, gamma?: number) => void;
}

export default function GammaSelector({ auto, gamma, onChange }: Props) {
  return (
    <div className="card-block">
      <h2 className="section-title">Регуляризация</h2>

      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={auto}
          onChange={(e) =>
            onChange(e.target.checked, e.target.checked ? undefined : gamma)
          }
        />
        Автоматический подбор γ
      </label>

      {!auto && (
        <input
          type="number"
          step="0.001"
          value={gamma ?? ""}
          placeholder="Введите γ"
          className="input"
          onChange={(e) => {
            const value = Number(e.target.value);
            onChange(false, Number.isFinite(value) ? value : undefined);
          }}
        />
      )}
    </div>
  );
}
