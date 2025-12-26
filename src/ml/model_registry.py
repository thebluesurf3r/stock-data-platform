import json
import os
import joblib
from datetime import datetime


class ModelRegistry:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def save(self, model, metadata: dict, version: str):
        model_path = f"{self.base_path}/{version}"
        os.makedirs(model_path, exist_ok=True)

        joblib.dump(model, f"{model_path}/model.pkl")

        metadata["saved_at"] = datetime.utcnow().isoformat()
        with open(f"{model_path}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
