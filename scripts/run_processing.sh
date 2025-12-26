#!/bin/bash
set -e

./venv/bin/python -m src.processing.clean_prices_job \
  --symbol INFY
