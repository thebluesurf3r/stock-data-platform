import os
from pyspark.sql import SparkSession


class SparkSessionFactory:
    """
    Factory for creating and managing SparkSession.
    """

    @staticmethod
    def create(app_name: str) -> SparkSession:
        """
        Create a SparkSession with sane local defaults.
        """

        # Force Spark to bind locally (prevents driver bind errors)
        os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

        spark = (
            SparkSession.builder
            .appName(app_name)
            .master("local[*]")
            .config("spark.driver.bindAddress", "127.0.0.1")
            .config("spark.driver.host", "127.0.0.1")
            .config("spark.driver.memory", "2g")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.ui.showConsoleProgress", "true")
            .getOrCreate()
        )

        spark.sparkContext.setLogLevel("WARN")
        return spark
