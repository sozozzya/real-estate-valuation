// src/components/ManualTableInput.tsx

import { useEffect, useState } from "react";
import type { Property } from "../types/apiTypes";

interface Props {
  onDataChange: (data: Property[]) => void;
}

export default function ManualTableInput({ onDataChange }: Props) {
  const [rows, setRows] = useState<Property[]>([
    { price: 0, house_area: 0, land_area: 0 },
  ]);

  useEffect(() => {
    onDataChange(rows);
  }, [rows, onDataChange]);

  const updateRow = (index: number, field: keyof Property, value: string) => {
    const numeric = Number(value);

    if (value === "" || Number.isNaN(numeric)) return;

    const updated = [...rows];

    updated[index] = {
      ...updated[index],
      [field]: numeric,
    };

    setRows(updated);
  };

  const addRow = () => {
    setRows([...rows, { price: 0, house_area: 0, land_area: 0 }]);
  };

  return (
    <div className="bg-white p-4 rounded shadow space-y-4">
      {rows.map((row, i) => (
        <div key={i} className="grid grid-cols-3 gap-2">
          <input
            type="number"
            placeholder="Цена"
            value={row.price}
            onChange={(e) => updateRow(i, "price", e.target.value)}
            className="border p-2"
          />

          <input
            type="number"
            placeholder="Площадь дома"
            value={row.house_area}
            onChange={(e) => updateRow(i, "house_area", e.target.value)}
            className="border p-2"
          />

          <input
            type="number"
            placeholder="Площадь участка"
            value={row.land_area}
            onChange={(e) => updateRow(i, "land_area", e.target.value)}
            className="border p-2"
          />
        </div>
      ))}

      <button onClick={addRow} className="bg-gray-200 px-3 py-1 rounded">
        Добавить строку
      </button>
    </div>
  );
}
