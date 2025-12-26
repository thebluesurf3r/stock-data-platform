📈 Stock Market Data Engineering & ML Platform

An end-to-end, production-style data engineering platform that ingests stock market data, processes it incrementally using Apache Spark, engineers features, trains machine learning models, and serves predictions via an API — all orchestrated with CI/CD.

This project is designed to demonstrate real-world Data Engineering practices.

🧠 Problem Statement

Stock market data is:

High volume

Time-series based

Continuously arriving

Used by downstream ML systems

This project solves the problem of building a scalable, incremental, and ML-ready data platform on a local system, without relying on paid cloud services.

🏗️ Architecture Overview
Raw CSV Data
    ↓
Ingestion Layer (OOP, Validation)
    ↓
Raw Zone (Partitioned Parquet)
    ↓
Processing Layer (Spark, Incremental)
    ↓
Curated Zone (Daily Prices)
    ↓
Feature Engineering (Technical Indicators)
    ↓
ML Training (scikit-learn)
    ↓
Model Registry (Versioned Artifacts)
    ↓
Prediction API (FastAPI)

1.1 Architecture Diagram (Text → Visual)
![Architecture](docs/architecture.png)
📐 Logical Architecture
                  ┌──────────────────────┐
                  │   CSV Stock Data     │
                  │ (Local / External)   │
                  └──────────┬───────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │ Ingestion Layer (Python) │
                │  - Validation            │
                │  - OOP Ingestors         │
                └──────────┬───────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ Raw Zone (Parquet, Partitioned)        │
        │ data/raw/stocks/symbol=...              │
        └──────────┬─────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ Processing Layer (Spark)                │
        │  - Incremental Processing               │
        │  - Metadata Watermarks                  │
        │  - Partition Pruning                    │
        └──────────┬─────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ Curated Zone (Daily Prices)             │
        │ data/curated/stocks/daily_prices        │
        └──────────┬─────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ Feature Engineering (Spark)             │
        │  - Returns                              │
        │  - Moving Averages                      │
        │  - Volatility                           │
        └──────────┬─────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ Feature Store (Indicators)              │
        │ data/curated/stocks/indicators          │
        └──────────┬─────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ ML Training (scikit-learn)              │
        │  - Logistic Regression                  │
        │  - Versioned Artifacts                  │
        └──────────┬─────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ Model Registry                          │
        │ models/stock_direction/v1               │
        └──────────┬─────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │ FastAPI Inference Service               │
        │  - /health                              │
        │  - /predict                             │
        └────────────────────────────────────────┘

🧱 Tech Stack
Data Engineering

Python

Apache Spark (PySpark)

Parquet

Partitioning & Partition Pruning

Incremental Processing with Metadata

Machine Learning

scikit-learn

Feature engineering with Spark window functions

Logistic Regression (baseline model)

Versioned model artifacts

DevOps / CI-CD

Jenkins

Bash-based orchestration scripts

Virtual environments

Git & GitHub

Serving

FastAPI

Model loaded once at startup

Stateless prediction API

📁 Project Structure
.
├── Jenkinsfile
├── requirements.txt
├── scripts/
│   ├── run_ingestion.sh
│   ├── run_processing.sh
│   ├── run_indicators.sh
│   ├── run_training.sh
│   └── smoke_tests.sh
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── ml/
│   ├── serving/
│   ├── utils/
│   └── validation/
└── test.py


⚠️ Data, models, and virtual environments are intentionally excluded from version control.

🔄 Incremental Processing Strategy

The pipeline uses metadata-driven watermarks to ensure:

Only new data is processed

Jobs are idempotent

Safe re-runs without duplication

Full-refresh mode available via CLI flags

Example:

python -m src.processing.clean_prices_job --symbol INFY
python -m src.processing.clean_prices_job --symbol INFY --full-refresh

📊 Feature Engineering

Technical indicators are computed using Spark window functions, including:

Daily returns

Moving averages (7, 14, 30)

Rolling volatility

These features are:

Computed incrementally

Partitioned by symbol / year / month

Optimized for downstream ML workloads

🤖 Machine Learning Pipeline

Feature dataset built from curated indicators

Binary classification target: next-day price direction

Model: Logistic Regression (baseline)

Training data capped to avoid Spark → Pandas memory issues

Artifacts saved with metadata

Example output:

models/stock_direction/v1/
├── model.pkl
└── metadata.json

🌐 Model Serving (FastAPI)

A lightweight prediction service exposes:

GET /health

POST /predict

Example request:

{
  "daily_return": 0.012,
  "ma_7": 1510.5,
  "ma_14": 1505.3,
  "ma_30": 1498.8,
  "volatility_14": 0.018
}


Response:

{
  "prediction": 1,
  "probability": 0.56,
  "model_version": "v1"
}

🔁 CI/CD with Jenkins

The Jenkins pipeline enforces:

Environment setup

Data ingestion

Spark processing

Feature engineering

Model training

Smoke tests

All steps are fully automated and fail-fast.

🚀 How to Run Locally
1️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2️⃣ Run pipeline manually
scripts/run_ingestion.sh
scripts/run_processing.sh
scripts/run_indicators.sh
scripts/run_training.sh

3️⃣ Start API
uvicorn src.serving.api:app --reload

🧪 Testing & Validation

Schema validation during ingestion

Value validation for stock prices

Smoke tests in CI

Partition pruning verified via Spark explain plans

🎯 Key Engineering Highlights

OOP + SOLID principles

Incremental Spark pipelines

Metadata-driven processing

Partition pruning optimization

Safe Spark → Pandas boundary handling

CI/CD automation

Clean Git hygiene

📌 Future Improvements

Dockerization

Nginx reverse proxy

Model version promotion

Feature drift detection

Backtesting framework

Cloud deployment (optional)

👤 Author

Built by thebluesurf3r
(Data Engineer | Python | Spark | ML Systems)