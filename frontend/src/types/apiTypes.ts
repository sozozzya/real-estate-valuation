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
  gamma?: number;
  auto_gamma?: boolean;
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
  gamma_used: number;
  n_observations: number;
  interpretation: Interpretation;
}
