from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("clickstream_batch_etl") \
    .getOrCreate()

# use HDFS now
df = spark.read.parquet("hdfs://namenode:8020/clickstream/stream")

top_pages = df.groupBy("page") \
              .agg(F.count("*").alias("views")) \
              .orderBy(F.desc("views"))

top_pages.show(20, truncate=False)

top_pages.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/shared/output/top_pages")

views_by_action = df.groupBy("action") \
                    .agg(F.count("*").alias("events")) \
                    .orderBy(F.desc("events"))

views_by_action.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/shared/output/views_by_action")
df = df.withColumn("day", F.to_date("ts"))

daily_events = df.groupBy("day") \
                 .agg(F.count("*").alias("events")) \
                 .orderBy("day")

daily_events.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/shared/output/daily_events")


print("Wrote CSV to /shared/output/top_pages")
spark.stop()
