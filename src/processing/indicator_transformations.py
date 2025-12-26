from pyspark.sql import DataFrame
from pyspark.sql.window import Window
from pyspark.sql.functions import (
    col,
    lag,
    avg,
    stddev,
    expr
)


def add_daily_returns(df: DataFrame) -> DataFrame:
    w = Window.partitionBy("symbol").orderBy("date")

    return df.withColumn(
        "daily_return",
        (col("close") - lag("close").over(w)) / lag("close").over(w)
    )


def add_moving_averages(df: DataFrame) -> DataFrame:
    w7 = Window.partitionBy("symbol").orderBy("date").rowsBetween(-6, 0)
    w14 = Window.partitionBy("symbol").orderBy("date").rowsBetween(-13, 0)
    w30 = Window.partitionBy("symbol").orderBy("date").rowsBetween(-29, 0)

    return (
        df
        .withColumn("ma_7", avg("close").over(w7))
        .withColumn("ma_14", avg("close").over(w14))
        .withColumn("ma_30", avg("close").over(w30))
    )


def add_rolling_volatility(df: DataFrame) -> DataFrame:
    w14 = Window.partitionBy("symbol").orderBy("date").rowsBetween(-13, 0)

    return df.withColumn(
        "volatility_14",
        stddev("daily_return").over(w14)
    )
