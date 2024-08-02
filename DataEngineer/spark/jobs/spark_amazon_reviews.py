import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Initialiser la session Spark
spark = SparkSession.builder \
    .appName("AmazonReviewsProcessing") \
    .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")) \
    .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")) \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Lire les données des ventes à partir de S3
df = spark.read.csv("s3a://salesdata7/amazon.csv", header=True, inferSchema=True)

# Nettoyer les données
df_cleaned = df.withColumn("discounted_price", when(col("discounted_price").isNull(), 0).otherwise(col("discounted_price")))

# Sauvegarder les données nettoyées dans un nouveau fichier sur S3 au format Parquet, compatible avec Athena
df_cleaned.write.parquet("s3a://salesdata7/cleaned_amazon_reviews/", mode="overwrite")

# Arrêter la session Spark
spark.stop()

