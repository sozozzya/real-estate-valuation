//src/pages/HomePage.tsx

import { useState } from "react";
import DataSourceSelector from "../components/DataSourceSelector";
import FileUpload from "../components/FileUpload";
import ManualTableInput from "../components/ManualTableInput";
import PriorInput from "../components/PriorInput";
import GammaSelector from "../components/GammaSelector";
import ResultsPanel from "../components/ResultsPanel";
import InterpretationPanel from "../components/InterpretationPanel";
import { useRidgeCalculation } from "../hooks/useRidgeCalculation";
import type { Property, CalculateResponse } from "../types/apiTypes";

export default function HomePage() {
  const [source, setSource] = useState<"file" | "manual">("file");
  const [properties, setProperties] = useState<Property[]>([]);
  const [betaPrior, setBetaPrior] = useState<number | undefined>();
  const [alphaPrior, setAlphaPrior] = useState<number | undefined>();
  const [autoGamma, setAutoGamma] = useState(true);
  const [gamma, setGamma] = useState<number | undefined>();
  const [result, setResult] = useState<CalculateResponse | null>(null);

  const { execute, loading, error } = useRidgeCalculation();

  const calculate = async () => {
    const cleaned = properties.filter(
      (p) =>
        Number.isFinite(p.price) &&
        Number.isFinite(p.house_area) &&
        Number.isFinite(p.land_area),
    );

    if (cleaned.length === 0) {
      alert("Нет корректных данных");
      return;
    }

    const res = await execute({
      properties: cleaned,
      beta_prior: betaPrior ?? 0,
      alpha_prior: alphaPrior ?? 0,
      gamma: autoGamma ? 0 : (gamma ?? 0),
      auto_gamma: autoGamma,
    });

    if (res) setResult(res);
  };

  return (
    <div className="app-container">
      <h1 className="page-title">Оценка удельной стоимости недвижимости</h1>

      <DataSourceSelector value={source} onChange={setSource} />

      {source === "file" ? (
        <FileUpload onDataLoaded={setProperties} />
      ) : (
        <ManualTableInput onDataChange={setProperties} />
      )}

      <PriorInput
        beta={betaPrior}
        alpha={alphaPrior}
        onChange={(b, a) => {
          setBetaPrior(b);
          setAlphaPrior(a);
        }}
      />

      <GammaSelector
        auto={autoGamma}
        gamma={gamma}
        onChange={(a, g) => {
          setAutoGamma(a);
          setGamma(g);
        }}
      />

      <button onClick={calculate} disabled={loading} className="primary-button">
        {loading ? "Выполняется расчет..." : "Рассчитать модель"}
      </button>

      {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}

      {result && (
        <>
          <ResultsPanel result={result} />
          <InterpretationPanel result={result} />
        </>
      )}
    </div>
  );
}
