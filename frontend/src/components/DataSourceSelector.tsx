//src/components/DataSourceSelector.tsx

interface Props {
  value: "file" | "manual";
  onChange: (v: "file" | "manual") => void;
}

export default function DataSourceSelector({ value, onChange }: Props) {
  return (
    <div className="bg-white p-4 rounded shadow space-y-3">
      <h2 className="font-semibold text-lg">Источник данных</h2>

      <div className="flex gap-4">
        <button
          type="button"
          onClick={() => onChange("file")}
          className={`px-4 py-2 rounded ${
            value === "file" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Загрузить файл
        </button>

        <button
          type="button"
          onClick={() => onChange("manual")}
          className={`px-4 py-2 rounded ${
            value === "manual" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Ввести вручную
        </button>
      </div>
    </div>
  );
}
