# src/application/mappers/input_mapper.py


from src.application.dto.calculate_input import CalculateRidgeInputDTO
from src.domain.models.property import Property
from src.domain.models.regression_data import RegressionData
from src.domain.models.ridge_prior import RidgePrior


class InputMapper:

    @staticmethod
    def to_domain(dto: CalculateRidgeInputDTO):

        properties = [
            Property(price=p.price, house_area=p.house_area, land_area=p.land_area)
            for p in dto.properties
        ]

        data = RegressionData(properties=properties)

        prior = RidgePrior(beta_prior=dto.beta_prior, alpha_prior=dto.alpha_prior)

        return data, prior
