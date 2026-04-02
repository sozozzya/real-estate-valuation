//src/pages/HomePage.tsx

import { useState } from "react";
import DataSourceSelector from "../components/DataSourceSelector";
import FileUpload from "../components/FileUpload";
import ManualTableInput from "../components/ManualTableInput";
import PriorInput from "../components/PriorInput";
import GammaSelector from "../components/GammaSelector";
import ResultsPanel from "../components/ResultsPanel";
import InterpretationPanel from "../components/InterpretationPanel";
import AnalysisPanel from "../components/AnalysisPanel";
import { useRidgeCalculation } from "../hooks/useRidgeCalculation";
import type { Property, CalculateResponse } from "../types/apiTypes";

export default function HomePage() {
  const [source, setSource] = useState<"file" | "manual">("file");
  const [properties, setProperties] = useState<Property[]>([]);
  const [betaPrior, setBetaPrior] = useState<number | undefined>();
  const [alphaPrior, setAlphaPrior] = useState<number | undefined>();
  const [autoLambda, setAutoLambda] = useState(true);
  const [lambdaBeta, setLambdaBeta] = useState<number | undefined>();
  const [lambdaAlpha, setLambdaAlpha] = useState<number | undefined>();
  const [result, setResult] = useState<CalculateResponse | null>(null);
  const [calculatedProperties, setCalculatedProperties] = useState<Property[]>([]);

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
      lambda_beta: autoLambda ? 0 : (lambdaBeta ?? 0),
      lambda_alpha: autoLambda ? 0 : (lambdaAlpha ?? 0),
      auto_lambda: autoLambda,
    });

    if (res) {
      setResult(res);
      setCalculatedProperties(cleaned);
    }
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
        auto={autoLambda}
        lambdaBeta={lambdaBeta}
        lambdaAlpha={lambdaAlpha}
        onChange={(a, lb, la) => {
          setAutoLambda(a);
          setLambdaBeta(lb);
          setLambdaAlpha(la);
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
          <AnalysisPanel properties={calculatedProperties} parameters={result.parameters} />
        </>
      )}
    </div>
  );
}
