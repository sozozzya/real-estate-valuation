import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
  showCalculatedLambdas: boolean;
}

export default function InterpretationPanel({ result, showCalculatedLambdas }: Props) {
  const { interpretation, lambda_star } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">🧠 Интерпретация и выводы</h2>
      <p>{interpretation.behavior}</p>
      <p>{interpretation.regularization_impact}</p>
      <p>{interpretation.market_change}</p>
      <p>{interpretation.forecast_reliability}</p>
      <p>{interpretation.limitations}</p>
      {showCalculatedLambdas && (
        <p>
          Подобранный параметр регуляризации: <b>λ* = {lambda_star.toFixed(4)}</b>
        </p>
      )}
    </div>
  );
}
