# src/infrastructure/data_readers/csv_reader.py

import csv
import logging

from src.application.dto.calculate_input import PropertyInputDTO
from src.application.ports.property_reader_port import PropertyReaderPort
from src.domain.exceptions import ValidationError

logger = logging.getLogger(__name__)


class CSVPropertyReader(PropertyReaderPort):

    REQUIRED_COLUMNS = {"price", "house_area", "land_area"}

    def read(self, file_path: str):

        logger.info("csv_read_started", file_path=file_path)

        try:
            with open(file_path, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                if not self.REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
                    raise ValidationError("csv file missing required columns")

                result = [
                    PropertyInputDTO(
                        price=float(r["price"]),
                        house_area=float(r["house_area"]),
                        land_area=float(r["land_area"]),
                    )
                    for r in reader
                ]

            logger.info(
                "csv_read_completed",
                file_path=file_path,
                n_records=len(result),
            )

            return result

        except FileNotFoundError as e:
            logger.warning(
                "csv_file_not_found",
                file_path=file_path,
                exc_info=True,
            )
            raise ValidationError("csv file not found") from e

        except ValueError as e:
            logger.warning(
                "csv_invalid_numeric_value",
                file_path=file_path,
                exc_info=True,
            )
            raise ValidationError("csv contains invalid numeric values") from e

        except ValidationError:
            logger.warning(
                "csv_validation_error",
                file_path=file_path,
                exc_info=True,
            )
            raise

        except Exception:
            logger.exception(
                "csv_unexpected_error",
                file_path=file_path,
            )
            raise
