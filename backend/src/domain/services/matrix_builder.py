# src/domain/services/matrix_builder.py

import numpy as np

from src.domain.models.regression_data import RegressionData


class MatrixBuilder:
    """
    Builds design matrix:

    V = βS + αQ + c
    """

    def build(self, data: RegressionData):

        X = np.array(
            [
                [p.house_area, p.land_area, 1.0]
                for p in data.properties
            ],
            dtype=float,
        )

        y = np.array(
            [p.price for p in data.properties],
            dtype=float
        )

        return X, y
