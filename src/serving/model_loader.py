import joblib
import json
from typing import Tuple


class ModelLoader:
    def __init__(self, model_base_path: str):
        self.model_base_path = model_base_path

    def load(self, version: str) -> Tuple[object, dict]:
        model_path = f"{self.model_base_path}/{version}"

        model = joblib.load(f"{model_path}/model.pkl")

        with open(f"{model_path}/metadata.json", "r") as f:
            metadata = json.load(f)

        return model, metadata
