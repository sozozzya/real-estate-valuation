from abc import ABC, abstractmethod
from typing import List

from src.application.dto.calculate_input import PropertyInputDTO


class PropertyReaderPort(ABC):

    @abstractmethod
    def read(self, file_path: str) -> List[PropertyInputDTO]:
        pass
