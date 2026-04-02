// src/components/InterpretationPanel.tsx

import { useMemo, useState } from "react";
import type { CalculateResponse } from "../types/apiTypes";

interface Props {
  result: CalculateResponse;
  showCalculatedLambdas: boolean;
}

const influenceLabel = (lambdaValue: number): string => {
  if (lambdaValue < 1) return "слабое";
  if (lambdaValue < 50) return "умеренное";
  return "высокое";
};

export default function InterpretationPanel({ result, showCalculatedLambdas }: Props) {
  const { lambda_beta_used, lambda_alpha_used, interpretation, uncertainty } = result;

  const uncertaintyWidth = Math.abs(uncertainty.beta_ci_95.upper - uncertainty.beta_ci_95.lower)
    + Math.abs(uncertainty.alpha_ci_95.upper - uncertainty.alpha_ci_95.lower);
  const reliabilityText = uncertaintyWidth > 200
    ? "Оценки имеют повышенную неопределённость из-за ограниченного объёма данных."
    : "Оценки параметров стабильны и находятся в разумных пределах.";

  return (
    <div className="result-card">
      <h2 className="result-title">🧠 Интерпретация</h2>
      <p>{interpretation.behavior}</p>
      <p>{interpretation.market_change}</p>
      <p>{reliabilityText}</p>
      <p>Использована регуляризация с учётом данных предыдущего периода.</p>
      <p>
        Влияние априорных данных: дом — <b>{influenceLabel(lambda_beta_used)}</b>,
        участок — <b>{influenceLabel(lambda_alpha_used)}</b>.
      </p>

      {showCalculatedLambdas && (
        <p>
          Автоматически рассчитанные параметры регуляризации: λβ = {lambda_beta_used.toFixed(2)}, λα = {lambda_alpha_used.toFixed(2)}.
        </p>
      )}
    </div>
  );
}
