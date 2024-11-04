# Data Streaming Project

In this project, we build a real-time data streaming pipeline that covers every phase, from data ingestion to processing and storage. The pipeline leverages a robust stack of tools and technologies, including Apache Airflow, Python, Apache Kafka, Apache Zookeeper, Apache Spark, and Cassandra, all efficiently containerized with Docker

## System architecture
![System_Architectur](https://github.com/user-attachments/assets/c5fac459-61d8-42aa-9cbd-d463b763f808)

### Apache Airflow:
Airflow orchestrates the data pipeline, managing and scheduling each task. It used to ensures that data flows seamlessly from ingestion to processing and finally to storage. With its DAG (Directed Acyclic Graph) structure, Airflow automates the workflow by triggering tasks in sequence or parallel based on dependencies.

### Python:
Python serves as the primary programming language for scripting custom logic within the pipeline. From defining Airflow tasks to developing data processing functions, Python is central to handling data extraction, transformation, and load (ETL) operations.

### Apache Kafka:
Kafka enables real-time data ingestion by acting as a message broker. Data is streamed to Kafka in near real-time, where it is temporarily held in a topic. This streaming architecture allows the pipeline to process large volumes of data quickly and efficiently.

### Apache Zookeeper: 
Zookeeper is used alongside Kafka to manage the distributed environment, handling tasks like leader election and maintaining configuration information for Kafka brokers. It ensures Kafka remains stable and reliable within the pipeline.

### Apache Spark:
Spark processes the ingested data, enabling complex transformations and computations in real-time. It connects to Kafka to consume data streams and performs operations like data cleaning, aggregation, and enrichment, which are essential for transforming raw data into valuable insights.

### Cassandra:
Cassandra serves as the storage solution for processed data. Known for its scalability and high write throughput, Cassandra allows the pipeline to store large amounts of processed data quickly and retrieve it efficiently for further analysis or visualization.

### Docker:
Docker containerizes each component of the pipeline, ensuring a consistent environment and simplifying deployment. Docker Compose is used to manage multi-container setups, allowing the entire stack—including Airflow, Kafka, Zookeeper, Spark, and Cassandra—to be orchestrated and run seamlessly in isolated containers.
