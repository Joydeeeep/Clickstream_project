

A complete end-to-end **real-time + batch clickstream analytics pipeline** built using:

* Apache Kafka – real-time event ingestion
* Apache Spark Structured Streaming – real-time processing
* Hadoop HDFS – distributed storage
* Spark Batch ETL – daily aggregations
* Apache Superset – visualization dashboard
* Docker Compose – containerized multi-service environment

This project simulates an **e-commerce clickstream pipeline** that ingests live events, processes them in real time, stores them in HDFS, and visualizes insights in dashboards.

---

## Architecture Overview

User Clicks → Kafka Producer → Kafka Topic → Spark Streaming → Spark Batch ETL → CSV
                                       
Superset Dashboard     

---

## Tech Stack

| Component       | Purpose                                           |
| --------------- | ------------------------------------------------- |
| Kafka           | Real-time ingestion of click events               |
| Spark Streaming | Processes incoming clickstream                    |
| HDFS (Hadoop)   | Distributed storage (Parquet files + checkpoints) |
| Spark Batch Job | Converts Parquet → CSV for analytics              |
| Superset        | Dashboard tool                                    |
| Docker          | Runs all services in isolated containers          |


---

# How to Run the Project (Commands Only)

### Start the entire environment

```
docker compose up -d
```

### Start Kafka clickstream producer

```
docker exec -it spark-master bash -lc "python /shared/producer/produce_clicks.py"
```

### Start Spark Streaming job

```
docker exec -it spark-master bash -lc "/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 --master spark://spark-master:7077 /shared/streaming/streaming_job.py"
```

### Start Spark Batch ETL job

```
docker exec -it spark-master bash -lc "/spark/bin/spark-submit --master spark://spark-master:7077 /shared/batch/batch_etl.py"
```

### Convert Parquet → CSV (if needed)

```
docker exec -it spark-master bash -lc "/spark/bin/spark-submit /shared/convert_parquet_to_csv.py"
```

---

# Dashboard (Superset)

### Access Superset UI:

```
http://localhost:8088
```

### Login:

```
username: admin
password: admin
```

### Steps to build dashboard:

1. Upload processed CSV file
2. Create a dataset
3. Build charts:

   * Hourly active users
   * Page views over time
   * Most viewed product pages
   * Session length patterns
4. Combine everything into a final dashboard

---

# What This Project Demonstrates

Real-time streaming analytics
Kafka–Spark integration
Distributed storage with HDFS
Batch processing workflow
Visual analytics with Superset
Docker-based big data environment

---

# Final Dashboard Insights

The dashboard shows:

* Active users per hour
* Real-time click rate
* Most viewed pages
* Geographic/device distribution
* Conversion metrics
* Session trends

---



