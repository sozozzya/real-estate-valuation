# src/infrastructure/data_readers/excel_reader.py

import logging
import pandas as pd

from src.application.dto.calculate_input import PropertyInputDTO
from src.domain.exceptions import ValidationError
from src.infrastructure.readers.base_reader import BasePropertyReader

logger = logging.getLogger(__name__)


class ExcelPropertyReader(BasePropertyReader):
    REQUIRED_COLUMNS = {"price", "house_area", "land_area"}

    def read(self, file_path: str):

        logger.info("excel_read_started", file_path=file_path)

        try:
            df = pd.read_excel(file_path)

            if not self.REQUIRED_COLUMNS.issubset(df.columns):
                raise ValidationError("excel file missing required columns")

            result = [
                PropertyInputDTO(
                    price=float(row["price"]),
                    house_area=float(row["house_area"]),
                    land_area=float(row["land_area"]),
                )
                for _, row in df.iterrows()
            ]

            logger.info(
                "excel_read_completed",
                file_path=file_path,
                n_records=len(result),
            )

            return result

        except FileNotFoundError as e:
            logger.warning(
                "excel_file_not_found",
                file_path=file_path,
                exc_info=True,
            )
            raise ValidationError("excel file not found") from e

        except ValueError as e:
            logger.warning(
                "excel_invalid_numeric_value",
                file_path=file_path,
                exc_info=True,
            )
            raise ValidationError("excel contains invalid numeric values") from e

        except ValidationError:
            logger.warning(
                "excel_validation_error",
                file_path=file_path,
                exc_info=True,
            )
            raise

        except Exception:
            logger.exception(
                "excel_unexpected_error",
                file_path=file_path,
            )
            raise
