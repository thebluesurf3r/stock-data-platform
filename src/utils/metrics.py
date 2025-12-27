import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY_URL = "localhost:9091"

logger = logging.getLogger(__name__)


def push_pipeline_metrics(
    job_name: str,
    stage: str,
    rows_processed: int,
    duration_seconds: float,
    status: str = "success",
):
    """
    Best-effort metrics push.
    This function MUST NEVER raise.
    """
    try:
        registry = CollectorRegistry()

        g_rows = Gauge(
            "pipeline_rows_processed",
            "Number of rows processed",
            ["job", "stage"],
            registry=registry,
        )

        g_duration = Gauge(
            "pipeline_duration_seconds",
            "Pipeline execution time",
            ["job", "stage"],
            registry=registry,
        )

        g_status = Gauge(
            "pipeline_status",
            "1 = success, 0 = failure",
            ["job", "stage"],
            registry=registry,
        )

        g_rows.labels(job_name, stage).set(float(rows_processed))
        g_duration.labels(job_name, stage).set(float(duration_seconds))
        g_status.labels(job_name, stage).set(1 if status == "success" else 0)

        push_to_gateway(
            PUSHGATEWAY_URL,
            job=job_name,
            registry=registry,
        )

    except Exception as e:
        # Metrics must NEVER crash the pipeline
        logger.warning(
            "Metrics push failed (non-fatal): %s", e
        )
