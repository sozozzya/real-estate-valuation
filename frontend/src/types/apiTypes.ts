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
  r2_loocv: number;
  rmse_loocv: number;
  mae_loocv: number;
  mape_loocv: number;
}

export interface ConfidenceInterval {
  lower: number;
  upper: number;
}

export interface Uncertainty {
  beta_ci_95: ConfidenceInterval;
  alpha_ci_95: ConfidenceInterval;
  beta_shift_pct: number;
  alpha_shift_pct: number;
  regularization_strength: string;
}

export interface Interpretation {
  behavior: string;
  regularization_impact: string;
  market_change: string;
  forecast_reliability: string;
  limitations: string;
}

export interface CvPoint {
  lambda_value: number;
  loocv_mse: number;
}

export interface Diagnostics {
  mean_residual: number;
}

export interface CalculateResponse {
  parameters: RegressionParameters;
  metrics: RegressionMetrics;
  uncertainty: Uncertainty;
  lambda_star: number;
  cv_curve: CvPoint[];
  diagnostics: Diagnostics;
  prediction_formula: string;
  n_observations: number;
  interpretation: Interpretation;
}
