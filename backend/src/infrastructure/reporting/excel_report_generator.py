# src/infrastructure/reporting/excel_report_generator.py

import logging
import pandas as pd

from src.application.ports.report_generator_port import ReportGeneratorPort

logger = logging.getLogger(__name__)


class ExcelReportGenerator(ReportGeneratorPort):

    def generate(self, result, output_path: str):

        logger.info(
            "excel_report_generation_started",
            output_path=output_path,
        )

        try:
            df = pd.DataFrame(
                {
                    "Metric": [
                        "Beta",
                        "Alpha",
                        "Beta Std Error",
                        "Alpha Std Error",
                        "Beta CI 95% Lower",
                        "Beta CI 95% Upper",
                        "Alpha CI 95% Lower",
                        "Alpha CI 95% Upper",
                        "RSS",
                        "MSE",
                        "RMSE",
                        "MAE",
                        "MAPE",
                        "R2",
                        "Lambda Beta",
                        "Lambda Alpha",
                    ],
                    "Value": [
                        result.parameters.beta,
                        result.parameters.alpha,
                        result.uncertainty.beta_standard_error,
                        result.uncertainty.alpha_standard_error,
                        result.uncertainty.beta_ci_95.lower,
                        result.uncertainty.beta_ci_95.upper,
                        result.uncertainty.alpha_ci_95.lower,
                        result.uncertainty.alpha_ci_95.upper,
                        result.metrics.rss,
                        result.metrics.mse,
                        result.metrics.rmse,
                        result.metrics.mae,
                        result.metrics.mape,
                        result.metrics.r2,
                        result.lambda_beta_used,
                        result.lambda_alpha_used,
                    ],
                }
            )

            df.to_excel(output_path, index=False)

            logger.info(
                "excel_report_generation_completed",
                output_path=output_path,
            )

        except Exception:
            logger.exception(
                "excel_report_generation_failed",
                output_path=output_path,
            )
            raise
