from pyspark.sql import DataFrame
from pyspark.sql.functions import lead, col
from pyspark.sql.window import Window


def build_training_dataset(df: DataFrame) -> DataFrame:
    """
    Builds features and label for ML training.
    Label: next-day price direction (1 = up, 0 = down)
    """

    w = Window.partitionBy("symbol").orderBy("date")

    df = df.withColumn(
        "next_close",
        lead("close").over(w)
    )

    df = df.withColumn(
        "label",
        (col("next_close") > col("close")).cast("int")
    )

    return df.dropna(subset=["label"])
