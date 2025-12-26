#!/bin/bash
set -e

python -m src.ingestion.ingest_job \
  --symbol INFY \
  --input_path data/sample_stock_data.csv
