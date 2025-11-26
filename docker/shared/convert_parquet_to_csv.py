from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ConvertParquetToCSV").getOrCreate()

# Read directly from HDFS where your streaming job wrote data
input_path = "hdfs://namenode:8020/clickstream/stream"
output_path = "/shared/clickstream_raw_csv"

print("Reading from:", input_path)
df = spark.read.parquet(input_path)

print("Schema:")
df.printSchema()

print("Sample rows:")
df.show(10)

print("Writing CSV to:", output_path)
df.write.csv(output_path, header=True, mode="overwrite")

print("Done.")
spark.stop()
