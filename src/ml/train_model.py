import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.processing.spark_session import SparkSessionFactory
from src.ml.feature_builder import build_training_dataset
from src.ml.model_registry import ModelRegistry
from pyspark.sql.functions import col

def train(symbol: str):
    spark = SparkSessionFactory.create("TrainStockModel")

    df = spark.read.parquet(
        "data/curated/stocks/indicators"
    ).filter(f"symbol = '{symbol}'")

    df = build_training_dataset(df)
    
    df = (
    df
        .orderBy(col("date").desc())
        .limit(10000)
    )

    feature_cols = [
        "daily_return",
        "ma_7",
        "ma_14",
        "ma_30",
        "volatility_14"
    ]

    pdf = df.select(feature_cols + ["label"]).toPandas()

    X = pdf[feature_cols]
    y = pdf["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"[INFO] Model accuracy: {acc:.4f}")

    registry = ModelRegistry("models/stock_direction")
    registry.save(
        model=model,
        version="v1",
        metadata={
            "symbol": symbol,
            "accuracy": acc,
            "features": feature_cols
        }
    )

    spark.stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    args = parser.parse_args()

    train(args.symbol)


if __name__ == "__main__":
    main()
