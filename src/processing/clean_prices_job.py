import argparse
from pyspark.sql.functions import col, lit, to_date

from src.processing.spark_session import SparkSessionFactory
from src.processing.transformations import cast_stock_columns, add_partitions
from src.utils.metadata_manager import MetadataManager


def run_clean_job(symbol: str, full_refresh: bool = False) -> None:
    spark = SparkSessionFactory.create("CleanStockPrices")

    raw_base_path = f"data/raw/stocks/symbol={symbol}"
    curated_path = "data/curated/stocks/daily_prices"
    metadata_path = "data/metadata/processed_ingestion_dates.json"

    metadata = MetadataManager(metadata_path)

    if full_refresh:
        print("[INFO] Running in FULL REFRESH mode")
        last_processed = None
    else:
        last_processed = metadata.get_last_processed_date(symbol)

    df_raw = spark.read.parquet(raw_base_path)

    if last_processed:
        print(f"[INFO] Last processed ingestion_date: {last_processed}")
        df_raw = df_raw.filter(
            col("ingestion_date") > to_date(lit(last_processed))
        )
    else:
        print("[INFO] No previous ingestion found. Full load.")

    if df_raw.limit(1).count() == 0:
        print("[INFO] No new data to process.")
        spark.stop()
        return

    df_clean = cast_stock_columns(df_raw)
    df_clean = add_partitions(df_clean)
    df_clean = df_clean.coalesce(2)

    (
        df_clean
        .write
        .mode("append")
        .partitionBy("symbol", "year", "month")
        .parquet(curated_path)
    )

    max_ingestion_date = (
        df_clean
        .selectExpr("max(ingestion_date) as max_date")
        .collect()[0]["max_date"]
        .isoformat()
    )

    metadata.update_last_processed_date(symbol, max_ingestion_date)

    spark.stop()
    print(f"[SUCCESS] Incremental data processed up to {max_ingestion_date}")
    
    if full_refresh:
        print("[INFO] Resetting metadata after full refresh")



def main():
    parser = argparse.ArgumentParser(description="Clean raw stock prices")

    parser.add_argument("--symbol", required=True)
    parser.add_argument(
        "--full-refresh",
        action="store_true",
        help="Reprocess all raw data and rebuild curated dataset"
    )

    args = parser.parse_args()
    run_clean_job(
        symbol=args.symbol,
        full_refresh=args.full_refresh
    )

    parser = argparse.ArgumentParser(description="Clean raw stock prices")
    parser.add_argument("--symbol", required=True)
    args = parser.parse_args()

    run_clean_job(symbol=args.symbol)


if __name__ == "__main__":
    main()
