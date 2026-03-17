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
  intercept: number;
}

export interface RegressionMetrics {
  mse: number;
  rmse: number;
  mae: number;
  r2: number;
}

export interface Interpretation {
  summary: string;
  quality: string;
}

export interface CalculateResponse {
  parameters: RegressionParameters;
  metrics: RegressionMetrics;
  lambda_beta_used: number;
  lambda_alpha_used: number;
  n_observations: number;
  interpretation: Interpretation;
}
