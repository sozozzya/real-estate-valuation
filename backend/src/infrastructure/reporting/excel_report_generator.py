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
                        "Intercept",
                        "MSE",
                        "RMSE",
                        "MAE",
                        "R2",
                        "Gamma",
                    ],
                    "Value": [
                        result.parameters.beta,
                        result.parameters.alpha,
                        result.parameters.intercept,
                        result.metrics.mse,
                        result.metrics.rmse,
                        result.metrics.mae,
                        result.metrics.r2,
                        result.gamma_used,
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
