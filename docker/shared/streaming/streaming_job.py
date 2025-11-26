from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StringType

spark = SparkSession.builder \
    .appName("clickstream_streaming") \
    .getOrCreate()

schema = StructType() \
    .add("user_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("page", StringType()) \
    .add("action", StringType())

# Read from Kafka topic "clickstream"
raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "clickstream") \
    .load()

json_df = raw.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# Convert timestamp to proper type
json_df = json_df.withColumn("ts", to_timestamp("timestamp"))

# Write streaming data into HDFS as Parquet
query = json_df.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/clickstream/stream") \
    .option("checkpointLocation", "hdfs://namenode:8020/clickstream/checkpoints") \
    .outputMode("append") \
    .start()


print("Streaming job started. Writing to hdfs://namenode:8020/clickstream/stream")
query.awaitTermination()
