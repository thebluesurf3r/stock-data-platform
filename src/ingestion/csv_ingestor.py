import os
import pandas as pd
from src.ingestion.base_ingestor import BaseIngestor


class CSVIngestor(BaseIngestor):
    """
    Ingest data from CSV files.
    """

    def __init__(self, symbol: str, file_path: str):
        super().__init__(symbol)
        self.file_path = file_path

    def read(self) -> pd.DataFrame:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(self.file_path)

        df = pd.read_csv(self.file_path)

        if df.empty:
            raise ValueError("CSV file is empty")

        return df
