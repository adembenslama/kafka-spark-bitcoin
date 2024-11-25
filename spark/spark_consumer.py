from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def create_spark_session():
    return SparkSession.builder \
        .appName("BitcoinPriceStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
        .getOrCreate()

def create_streaming_query(spark):
    print("Initializing streaming query...")
    # Définir le schéma des messages
    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("price_usd", DoubleType(), True),
        StructField("price_eur", DoubleType(), True)
    ])

    print("Creating Kafka stream...")
    # Lire le flux de données depuis Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "machine_learning") \
        .option("startingOffsets", "earliest") \
        .load()

    print("Processing stream...")
    # Convertir et traiter les messages
    prices = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select(
            "data.timestamp",
            "data.price_usd",
            "data.price_eur"
        )

    # Afficher les messages
    return prices \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .option("numRows", 10) \
        .start()

if __name__ == "__main__":
    spark = create_spark_session()
    query = create_streaming_query(spark)
    query.awaitTermination() 