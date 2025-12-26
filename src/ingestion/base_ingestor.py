from abc import ABC, abstractmethod
import pandas as pd


class BaseIngestor(ABC):
    """
    Abstract base class for all ingestion sources.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol

    @abstractmethod
    def read(self) -> pd.DataFrame:
        """Read data from source"""
        pass

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add standard metadata"""
        from datetime import datetime

        df["symbol"] = self.symbol
        df["ingestion_timestamp"] = datetime.utcnow()
        return df
