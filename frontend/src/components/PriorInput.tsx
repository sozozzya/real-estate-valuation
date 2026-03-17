//src/components/PriorInput.tsx

interface Props {
  beta?: number;
  alpha?: number;
  onChange: (beta?: number, alpha?: number) => void;
}

export default function PriorInput({ beta, alpha, onChange }: Props) {
  return (
    <div className="bg-white p-4 rounded shadow space-y-3">
      <h2 className="font-semibold">Предыдущие оценки (опционально)</h2>

      <input
        type="number"
        placeholder="β₀ (удельная стоимость дома)"
        className="border p-2 w-full"
        onChange={(e) =>
          onChange(
            e.target.value === "" ? undefined : Number(e.target.value),
            alpha,
          )
        }
      />

      <input
        type="number"
        placeholder="α₀ (удельная стоимость участка)"
        className="border p-2 w-full"
        onChange={(e) =>
          onChange(
            beta,
            e.target.value === "" ? undefined : Number(e.target.value),
          )
        }
      />
    </div>
  );
}
