from abc import ABC, abstractmethod

from src.application.dto.calculate_result import CalculateRidgeResultDTO


class ReportGeneratorPort(ABC):

    @abstractmethod
    def generate(self, result: CalculateRidgeResultDTO, output_path: str) -> None:
        pass
