import os
import argparse
import time

from src.utils.metrics import push_pipeline_metrics
from src.ingestion.csv_ingestor import CSVIngestor
from src.utils.paths import raw_stock_path
from src.validation.stock_schema_validator import StockSchemaValidator
from src.validation.stock_value_validator import StockValueValidator


def run_ingestion(ingestor, output_base: str) -> int:
    df = ingestor.read()

    validators = [
        StockSchemaValidator(),
        StockValueValidator()
    ]

    for validator in validators:
        validator.validate(df)

    df = ingestor.enrich(df)

    output_path = raw_stock_path(output_base, ingestor.symbol)
    os.makedirs(output_path, exist_ok=True)

    output_file = f"{output_path}/data.parquet"
    df.to_parquet(output_file, index=False)

    # ✅ CORRECT row count handling
    if hasattr(df, "rdd"):          # Spark DataFrame
        rows_written = df.count()
    else:                           # Pandas DataFrame
        rows_written = len(df)

    print(f"[SUCCESS] Data written to {output_file} ({rows_written} rows)")

    return rows_written


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Stock data ingestion job")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--input_path", required=True)

    args = parser.parse_args()

    ingestor = CSVIngestor(
        symbol=args.symbol,
        file_path=args.input_path
    )

    try:
        rows_written = run_ingestion(
            ingestor=ingestor,
            output_base="data/raw/stocks"
        )

        duration = time.time() - start_time

        # Emit metrics ONLY after successful commit
        push_pipeline_metrics(
            job_name="stock_pipeline",
            stage="ingestion",
            rows_processed=rows_written,
            duration_seconds=duration,
            status="success",
        )

    except Exception:
        duration = time.time() - start_time

        # Failure metric (best-effort)
        push_pipeline_metrics(
            job_name="stock_pipeline",
            stage="ingestion",
            rows_processed=0,
            duration_seconds=duration,
            status="failure",
        )

        raise


if __name__ == "__main__":
    main()
