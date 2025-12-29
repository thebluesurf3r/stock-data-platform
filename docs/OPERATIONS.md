✅ DAILY CHECKS (10–15 minutes)
1️⃣ Jenkins – Did the pipeline run?

Goal: Ensure the pipeline is executing as expected.

Checklist:

 Jenkins pipeline ran today

 No red stages in the last run

 No unexpected retries

 Duration is within normal range

If broken:

Open Jenkins console logs

Identify failing stage (Ingestion / Processing / Indicators / Training)

Do not rerun blindly — inspect first

2️⃣ Ingestion Health

Goal: Confirm raw data ingestion is correct and complete.

Checks:

 New folder exists under
data/raw/stocks/symbol=XYZ/ingestion_date=YYYY-MM-DD/

 data.parquet exists

 Row count > 0

 No schema validation failures

Command:

ls data/raw/stocks/symbol=INFY


If broken:

Check input source (CSV / API)

Re-run ingestion only, not full pipeline

Verify metadata not updated on failure

3️⃣ Processing & Indicators

Goal: Ensure transformations ran fully.

Checks:

 Curated data exists under data/curated/stocks/

 Indicator columns present

 No partial writes

 No stale partitions

Command:

ls data/curated/stocks/symbol=INFY


If broken:

Check Spark logs

Verify partition pruning logic

Confirm incremental filters are correct

4️⃣ Metadata & Incremental State (CRITICAL)

Goal: Ensure pipeline state is truthful.

Files to inspect:

data/metadata/processed_ingestion_dates.json

data/metadata/processed_indicators.json

Checks:

 Watermark moved forward

 No rollback

 No update on failed runs

Golden rule:

If data write failed, metadata must not change

If broken:

Restore metadata from backup or git

Run full refresh if state is corrupted

5️⃣ Observability (Grafana / Prometheus)

Goal: Detect silent failures early.

Checks in Grafana:

 Pipeline status = SUCCESS

 Rows processed > 0

 Duration not spiking

 No missing runs

If metrics missing:

Check Pushgateway

Re-run one job

Confirm Prometheus target is UP

🗓 WEEKLY CHECKS (30–45 minutes)
6️⃣ Trend Analysis

Goal: Catch slow degradation.

Checks:

 Pipeline duration trending stable

 Data volume consistent week-over-week

 No gradual slowdown

 No rising failure rate

If drifting:

Investigate data growth

Check Spark config

Re-evaluate partitioning

7️⃣ Data Quality Sanity

Goal: Prevent garbage-in, garbage-out.

Checks:

 Null % stable for critical columns

 No extreme spikes/drops

 No duplicate explosion

Optional commands:

df.isnull().mean()
df.duplicated().mean()


If broken:

Pause downstream jobs

Fix upstream ingestion

Backfill if needed

8️⃣ Disk & Storage Health

Goal: Avoid silent disk failures.

Checks:

 Disk usage < 80%

 No excessive small files

 Old raw data archived or purged

Command:

df -h
du -sh data/

🚨 ON-DEMAND / INCIDENT RESPONSE
Scenario: Pipeline failed

Steps:

Identify failing stage in Jenkins

Check logs for root cause

Verify:

data not partially written

metadata not advanced

Fix issue

Rerun only the failed stage

Never:

❌ Delete data blindly

❌ Reset metadata first

❌ Rerun everything without understanding

Scenario: Metrics missing but jobs succeeded

Likely causes:

Pushgateway down

Prometheus restart

Time range mismatch

Actions:

Restart observability stack

Re-run one job

Ignore historical gaps (metrics are best-effort)

Scenario: Incremental state corrupted

Recovery:

Stop all downstream jobs

Inspect metadata files

Restore last known good state

Run full refresh with CLI flag

Resume incremental runs

🔁 MONTHLY MAINTENANCE

 Review Jenkinsfile for cleanup

 Remove unused scripts

 Validate README accuracy

 Backup metadata

 Review alerts & thresholds

🧠 Operational Rules (Non-Negotiable)

Metrics never block business logic

Metadata updates only after success

Incremental pipelines must be restart-safe

Observability is part of the pipeline

Silent failure is worse than loud failure

🧪 Pre-Release Checklist (before changes)

Before merging changes:

 Run ingestion standalone

 Run processing standalone

 Validate metadata behavior

 Confirm metrics still emit

 Update this helpbook if behavior changes
