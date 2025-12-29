🧰 Stock Data Platform — Operations Command Playbook

All commands assume repo root unless stated otherwise.

🔁 DAILY OPERATIONS (10–15 min)
1️⃣ Jenkins – Did the pipeline run?
Check Jenkins service
systemctl status jenkins

Check Jenkins is listening
ss -lntp | grep 8080

Tail Jenkins logs (if needed)
sudo journalctl -u jenkins -n 200 --no-pager

2️⃣ Ingestion – Raw data health
Check raw data folders
ls -lh data/raw/stocks/

Check latest ingestion date
ls -lt data/raw/stocks/symbol=INFY/

Check parquet file exists
ls data/raw/stocks/symbol=INFY/ingestion_date=*/data.parquet

Quick row count (Pandas)
python - <<EOF
import pandas as pd
df = pd.read_parquet("data/raw/stocks/symbol=INFY/ingestion_date=2025-12-27/data.parquet")
print(len(df))
EOF

3️⃣ Processing & Indicators – Curated layer
Check curated output
ls -lh data/curated/stocks/

Inspect columns
python - <<EOF
import pandas as pd
df = pd.read_parquet("data/curated/stocks/symbol=INFY/data.parquet")
print(df.columns)
EOF

Validate indicator presence
python - <<EOF
expected = {"rsi", "macd", "sma_20"}
df = pd.read_parquet("data/curated/stocks/symbol=INFY/data.parquet")
print(expected.issubset(set(df.columns)))
EOF

4️⃣ Metadata & Incremental State (CRITICAL)
Inspect ingestion watermark
cat data/metadata/processed_ingestion_dates.json | jq .

Inspect indicators watermark
cat data/metadata/processed_indicators.json | jq .

Diff metadata vs last run
git diff data/metadata/

5️⃣ Observability – Prometheus / Grafana
Check containers
docker ps

Check Prometheus UI
curl http://localhost:9090/-/healthy

Check Pushgateway
curl http://localhost:9091

Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq .

Query metrics directly
curl "http://localhost:9090/api/v1/query?query=pipeline_status"

📊 WEEKLY OPERATIONS
6️⃣ Trend checks (volume & duration)
Check recent metric samples
curl "http://localhost:9090/api/v1/query?query=pipeline_duration_seconds"

Check row trends
curl "http://localhost:9090/api/v1/query?query=pipeline_rows_processed"

7️⃣ Data quality sanity
Null percentage
python - <<EOF
import pandas as pd
df = pd.read_parquet("data/curated/stocks/symbol=INFY/data.parquet")
print(df.isnull().mean())
EOF

Duplicate rate
python - <<EOF
import pandas as pd
df = pd.read_parquet("data/curated/stocks/symbol=INFY/data.parquet")
print(df.duplicated().mean())
EOF

8️⃣ Disk & storage
Disk usage
df -h

Data directory size
du -sh data/

Find large files
find data/ -type f -size +500M

🚨 INCIDENT RESPONSE COMMANDS
Scenario: Pipeline failed
Re-run only ingestion
python -m src.ingestion.ingest_job \
  --symbol INFY \
  --input_path data/sample_stock_data.csv

Re-run processing
bash scripts/run_processing.sh

Re-run indicators
bash scripts/run_indicators.sh

Scenario: Metrics missing
Restart observability stack
cd observability
docker-compose down
docker-compose up -d

Re-push metrics
python -m src.ingestion.ingest_job \
  --symbol INFY \
  --input_path data/sample_stock_data.csv

Scenario: Incremental state corrupted
Backup metadata
cp -r data/metadata data/metadata_backup_$(date +%F)

Reset metadata (ONLY if full refresh)
rm data/metadata/processed_ingestion_dates.json
rm data/metadata/processed_indicators.json

Full refresh (example)
bash scripts/run_processing.sh --full-refresh

🔁 MONTHLY MAINTENANCE
Clean unused Docker resources
docker system prune

Stop all project services
docker-compose down
sudo systemctl stop jenkins

Restart clean
sudo systemctl start docker
sudo systemctl start jenkins

🧪 PRE-CHANGE CHECKS
bash scripts/smoke_tests.sh

pytest

🧠 ONE COMMAND TO SEE EVERYTHING RUNNING
ps aux | egrep "python|spark|docker|jenkins"
