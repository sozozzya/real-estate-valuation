//src/types/apiTypes.ts

export interface Property {
  price: number;
  house_area: number;
  land_area: number;
}

export interface CalculateRequest {
  properties: Property[];
  beta_prior?: number;
  alpha_prior?: number;
  lambda_beta?: number;
  lambda_alpha?: number;
  auto_lambda?: boolean;
}

export interface RegressionParameters {
  beta: number;
  alpha: number;
}

export interface RegressionMetrics {
  rss: number;
  mse: number;
  rmse: number;
  mae: number;
  mape: number;
  r2: number;
}

export interface ConfidenceInterval {
  lower: number;
  upper: number;
}

export interface Uncertainty {
  beta_standard_error: number;
  alpha_standard_error: number;
  beta_ci_95: ConfidenceInterval;
  alpha_ci_95: ConfidenceInterval;
}

export interface Interpretation {
  behavior: string;
  market_change: string;
  quality: string;
}

export interface CalculateResponse {
  parameters: RegressionParameters;
  metrics: RegressionMetrics;
  uncertainty: Uncertainty;
  lambda_beta_used: number;
  lambda_alpha_used: number;
  prediction_formula: string;
  n_observations: number;
  interpretation: Interpretation;
}
