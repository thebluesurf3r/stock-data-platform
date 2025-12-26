import pandas as pd
from src.validation.base_validator import BaseValidator


class StockValueValidator(BaseValidator):
    """
    Validates basic sanity rules for stock values.
    """

    def validate(self, df: pd.DataFrame) -> None:
        if (df["open"] < 0).any():
            raise ValueError("Validation failed: Negative open price detected")

        if (df["close"] < 0).any():
            raise ValueError("Validation failed: Negative close price detected")

        if (df["high"] < df["low"]).any():
            raise ValueError("Validation failed: high < low detected")

        if (df["volume"] < 0).any():
            raise ValueError("Validation failed: Negative volume detected")
