from src.processing.spark_session import SparkSessionFactory

spark = SparkSessionFactory.create("SparkSessionTest")

df = spark.range(5)
df.show()

spark.stop()
