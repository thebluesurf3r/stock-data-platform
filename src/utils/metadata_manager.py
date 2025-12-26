import json
import os
from typing import Optional


class MetadataManager:
    """
    Manages pipeline metadata for incremental processing.
    """

    def __init__(self, metadata_path: str):
        self.metadata_path = metadata_path

    def get_last_processed_date(self, symbol: str):
        if not os.path.exists(self.metadata_path):
            return None

        try:
            with open(self.metadata_path, "r") as f:
                content = f.read().strip()

                if not content:
                    # Empty file
                    return None

                data = json.loads(content)

            return data.get(symbol)

        except json.JSONDecodeError:
            # Corrupt or partial metadata file
            return None


    def update_last_processed_date(self, symbol: str, ingestion_date: str) -> None:
        data = {}

        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
            except json.JSONDecodeError:
                # Corrupt metadata, start fresh
                data = {}

        data[symbol] = ingestion_date

        os.makedirs(os.path.dirname(self.metadata_path), exist_ok=True)

        with open(self.metadata_path, "w") as f:
            json.dump(data, f, indent=2)

