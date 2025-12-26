#!/bin/bash
set -e

python -m src.processing.clean_prices_job \
  --symbol INFY
