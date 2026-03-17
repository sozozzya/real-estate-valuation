// src/components/FileUpload.tsx

import { useState } from "react";
import type { Property } from "../types/apiTypes";

interface Props {
  onDataLoaded: (data: Property[]) => void;
}

export default function FileUpload({ onDataLoaded }: Props) {
  const [error, setError] = useState<string | null>(null);

  const handleFile = async (file: File) => {
    try {
      setError(null);

      const text = await file.text();

      const rows = text
        .replace(/^\uFEFF/, "")
        .split(/\r?\n/)
        .map((r) => r.trim())
        .filter(Boolean);

      if (rows.length < 2) {
        throw new Error("Файл не содержит данных");
      }

      const parsed: Property[] = rows.slice(1).map((r, index) => {
        const cols = r.split(/[;,]/).map((v) => v.trim());

        if (cols.length < 3) {
          throw new Error(`Ошибка формата строки ${index + 2}`);
        }

        const price = Number(cols[0]);
        const house = Number(cols[1]);
        const land = Number(cols[2]);

        if (
          !Number.isFinite(price) ||
          !Number.isFinite(house) ||
          !Number.isFinite(land)
        ) {
          throw new Error(`Ошибка чисел в строке ${index + 2}`);
        }

        return {
          price,
          house_area: house,
          land_area: land,
        };
      });

      onDataLoaded(parsed);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка чтения файла");
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow space-y-3">
      <input
        type="file"
        accept=".csv"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
        }}
      />

      {error && <p className="text-red-500">{error}</p>}
    </div>
  );
}
