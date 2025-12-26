import argparse
from pyspark.sql.functions import col, lit, to_date

from src.processing.spark_session import SparkSessionFactory
from src.processing.indicator_transformations import (
    add_daily_returns,
    add_moving_averages,
    add_rolling_volatility
)
from src.utils.metadata_manager import MetadataManager


def run_indicator_job(symbol: str, full_refresh: bool = False) -> None:
    spark = SparkSessionFactory.create("ComputeStockIndicators")

    curated_prices_path = "data/curated/stocks/daily_prices"
    indicators_path = "data/curated/stocks/indicators"
    metadata_path = "data/metadata/processed_indicators.json"

    metadata = MetadataManager(metadata_path)

    if full_refresh:
        print("[INFO] Running INDICATORS in FULL REFRESH mode")
        last_processed = None
    else:
        last_processed = metadata.get_last_processed_date(symbol)

    df = spark.read.parquet(curated_prices_path).filter(
        col("symbol") == symbol
    )

    if last_processed:
        print(f"[INFO] Last indicator date: {last_processed}")
        df = df.filter(col("date") > to_date(lit(last_processed)))

    if df.limit(1).count() == 0:
        print("[INFO] No new data for indicators.")
        spark.stop()
        return

    df = add_daily_returns(df)
    df = add_moving_averages(df)
    df = add_rolling_volatility(df)

    (
        df
        .write
        .mode("append")
        .partitionBy("symbol", "year", "month")
        .parquet(indicators_path)
    )

    max_date = (
        df
        .selectExpr("max(date) as max_date")
        .collect()[0]["max_date"]
        .isoformat()
    )

    metadata.update_last_processed_date(symbol, max_date)

    spark.stop()
    print(f"[SUCCESS] Indicators processed up to {max_date}")

def main():
    parser = argparse.ArgumentParser(
        description="Compute incremental stock indicators"
    )

    parser.add_argument("--symbol", required=True)
    parser.add_argument(
        "--full-refresh",
        action="store_true",
        help="Recompute all indicators from scratch"
    )

    args = parser.parse_args()

    run_indicator_job(
        symbol=args.symbol,
        full_refresh=args.full_refresh
    )


if __name__ == "__main__":
    main()
