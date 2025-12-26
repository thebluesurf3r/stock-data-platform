from src.processing.spark_session import SparkSessionFactory

spark = SparkSessionFactory.create("ExplainPartitionPruning")

(
    spark.read
    .parquet("data/curated/stocks/daily_prices")
    .filter("symbol = 'INFY' AND year = 2025 AND month = 12")
    .explain(True)
)

spark.stop()
