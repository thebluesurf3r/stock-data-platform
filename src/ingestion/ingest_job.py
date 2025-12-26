import os
import argparse

from src.ingestion.csv_ingestor import CSVIngestor
from src.utils.paths import raw_stock_path
from src.validation.stock_schema_validator import StockSchemaValidator
from src.validation.stock_value_validator import StockValueValidator


def run_ingestion(ingestor, output_base: str) -> None:
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

    print(f"[SUCCESS] Data written to {output_file}")



def main():
    parser = argparse.ArgumentParser(description="Stock data ingestion job")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--input_path", required=True)

    args = parser.parse_args()

    ingestor = CSVIngestor(
        symbol=args.symbol,
        file_path=args.input_path
    )

    run_ingestion(
        ingestor=ingestor,
        output_base="data/raw/stocks"
    )


if __name__ == "__main__":
    main()
