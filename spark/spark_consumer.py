from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

def create_spark_session():
    return SparkSession.builder \
        .appName("KafkaSparkStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
        .getOrCreate()

def create_streaming_query(spark):
    # Définir le schéma des messages
    schema = StructType([
        StructField("message", StringType(), True)
    ])

    # Lire le flux de données depuis Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "machine_learning") \
        .load()

    # Convertir et traiter les messages
    messages = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.message")

    # Afficher les messages
    return messages \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

if __name__ == "__main__":
    spark = create_spark_session()
    query = create_streaming_query(spark)
    query.awaitTermination() 