# Databricks notebook source
# Definición de las rutas de S3 y creación de datos de prueba
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import current_timestamp, col, sha2, trim
import datetime

BRONZE_PATH = "s3a://jocelyn-lakehouse-bronze/data/"
SILVER_PATH = "s3a://jocelyn-lakehouse-silver/data/"
GOLD_PATH = "s3a://jocelyn-lakehouse-gold/data/"

# 1. Crear dataset sintético simulando la llegada de datos de clientes
data = [
    ("C101", "  juan.perez@email.com ", "2026-08-21 10:00:00"),
    ("C102", "maria.gomez@email.com", "2026-08-21 10:15:00"),
    ("C103", "carlos.lopez@domain.com", "2026-08-21 10:30:00"),
    ("C104", "correo_invalido_sin_arroba", "2026-08-21 10:45:00")
]

schema = ["customer_id", "email", "created_at"]
df_input = spark.createDataFrame(data, schema)

print("Datos de entrada cargados en memoria:")
display(df_input)

# COMMAND ----------

# Guardar en Capa BRONZE en formato Delta Lake
df_bronze = df_input.withColumn("ingested_at", current_timestamp())

# Guardar en Delta Lake (almacenamiento local del Lakehouse / S3)
df_bronze.write.format("delta").mode("overwrite").saveAsTable("bronze_customers")

print("Capa BRONZE procesada exitosamente:")
display(spark.read.table("bronze_customers"))

# COMMAND ----------

# Leer de Bronze, limpiar espacios y enmascarar correo electrónico (PII)
df_bronze_read = spark.read.table("bronze_customers")

df_silver = df_bronze_read \
    .filter(col("email").contains("@")) \
    .withColumn("customer_id", trim(col("customer_id"))) \
    .withColumn("hashed_email", sha2(trim(col("email")), 256)) \
    .select("customer_id", "hashed_email", "created_at", "ingested_at")

df_silver.write.format("delta").mode("overwrite").saveAsTable("silver_customers")

print("Capa SILVER procesada (Emails anonimizados y registros filtrados):")
display(spark.read.table("silver_customers"))

# COMMAND ----------

# Crear vista de agregación para dashboards/negocio
df_silver_read = spark.read.table("silver_customers")

df_gold = df_silver_read.groupBy("created_at") \
    .count() \
    .withColumnRenamed("count", "total_registros")

df_gold.write.format("delta").mode("overwrite").saveAsTable("gold_daily_summary")

print("Capa GOLD finalizada:")
display(spark.read.table("gold_daily_summary"))