import pandas as pd
from src.validation.base_validator import BaseValidator


class StockSchemaValidator(BaseValidator):
    """
    Validates presence and basic types of stock data columns.
    """

    REQUIRED_COLUMNS = {
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume"
    }

    def validate(self, df: pd.DataFrame) -> None:
        if df.empty:
            raise ValueError("Validation failed: DataFrame is empty")

        missing_columns = self.REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"Validation failed: Missing columns {missing_columns}"
            )
