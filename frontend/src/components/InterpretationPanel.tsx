import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
  showCalculatedLambdas: boolean;
}

export default function InterpretationPanel({ result, showCalculatedLambdas }: Props) {
  const { interpretation, lambda_star } = result;

  return (
    <div className="result-card">
      <h2 className="result-title">🧠 Интерпретация</h2>
      <p>{interpretation.behavior}</p>
      <p>{interpretation.market_change}</p>
      <p>{interpretation.reliability}</p>
      {showCalculatedLambdas && (
        <p>
          Подобранный параметр регуляризации: <b>λ* = {lambda_star.toFixed(4)}</b>
        </p>
      )}
    </div>
  );
}
