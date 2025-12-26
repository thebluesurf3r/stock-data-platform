from abc import ABC, abstractmethod
import pandas as pd


class BaseValidator(ABC):
    """
    Base class for all data validators.
    Validators must raise exceptions on failure.
    """

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> None:
        """
        Validate input DataFrame.

        :param df: Pandas DataFrame to validate
        :raises ValueError: if validation fails
        """
        pass
