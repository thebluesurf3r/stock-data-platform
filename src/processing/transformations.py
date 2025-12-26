from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    to_date,
    year,
    month
)


def cast_stock_columns(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn("date", to_date(col("date")))
        .withColumn("open", col("open").cast("double"))
        .withColumn("high", col("high").cast("double"))
        .withColumn("low", col("low").cast("double"))
        .withColumn("close", col("close").cast("double"))
        .withColumn("volume", col("volume").cast("long"))
    )


def add_partitions(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn("year", year(col("date")))
        .withColumn("month", month(col("date")))
    )
