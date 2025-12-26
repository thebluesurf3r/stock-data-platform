from datetime import datetime


def raw_stock_path(base_path: str, symbol: str) -> str:
    ingestion_date = datetime.utcnow().strftime("%Y-%m-%d")
    return f"{base_path}/symbol={symbol}/ingestion_date={ingestion_date}"
