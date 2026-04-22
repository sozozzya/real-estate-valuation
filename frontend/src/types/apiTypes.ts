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
  mse: number;
  rmse: number;
  mae: number;
}

export interface ConfidenceInterval {
  lower: number;
  upper: number;
}

export interface Uncertainty {
  beta_ci_95: ConfidenceInterval;
  alpha_ci_95: ConfidenceInterval;
}

export interface Interpretation {
  behavior: string;
  market_change: string;
  reliability: string;
}

export interface SplitInfo {
  train_size: number;
  test_size: number;
}

export interface CvPoint {
  lambda_value: number;
  loocv_mse: number;
}

export interface CalculateResponse {
  parameters: RegressionParameters;
  metrics: RegressionMetrics;
  uncertainty: Uncertainty;
  lambda_star: number;
  split: SplitInfo;
  cv_curve: CvPoint[];
  prediction_formula: string;
  n_observations: number;
  interpretation: Interpretation;
}
