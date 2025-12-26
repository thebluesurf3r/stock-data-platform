#!/bin/sh

set -e

./venv/bin/python -m src.processing.compute_indicators_job --symbol INFY
