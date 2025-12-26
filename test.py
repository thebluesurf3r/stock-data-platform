import os
from pyspark.sql import SparkSession

# Force Spark to bind locally
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

spark = (
    SparkSession.builder
    .appName("StockDataPlatform")
    .master("local[*]")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.driver.host", "127.0.0.1")
    .getOrCreate()
)

data = [
    ("INFY", "2025-01-01", 1500.0),
    ("INFY", "2025-01-02", 1520.0)
]

df = spark.createDataFrame(data, ["symbol", "date", "close_price"])
df.show()

df.write.mode("overwrite").parquet("data/test_output")

spark.stop()
