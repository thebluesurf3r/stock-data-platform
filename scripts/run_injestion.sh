#!/bin/bash

./venv/bin/python -m src.ingestion.ingest_job \
  --symbol INFY \
  --input_path data/sample_stock_data.csv