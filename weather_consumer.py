import json
import psycopg2
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime
from datetime import datetime

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("WeatherDataProcessing") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.20") \
    .getOrCreate()

# PostgreSQL Configuration
DB_NAME = "weather_db"
DB_USER = "admin"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Kafka Configuration
KAFKA_TOPIC = "weather_data"
KAFKA_SERVER = "localhost:9092"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()

# Create Table (if not exists)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id SERIAL PRIMARY KEY,
        city TEXT,
        temperature_c FLOAT,
        temperature_f FLOAT,
        humidity INT,
        weather TEXT,
        timestamp_utc TIMESTAMP
    )
""")
conn.commit()

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("Listening for weather data...")

data_list = []  # Temporary list for batch processing

for message in consumer:
    weather_data = message.value
    print(f"Received: {weather_data}")

    # Append received data to list
    data_list.append((
        weather_data["city"],
        weather_data["temperature"],
        (weather_data["temperature"] * 9/5) + 32,  # Convert Celsius to Fahrenheit
        weather_data["humidity"],
        weather_data["weather"],
        datetime.utcfromtimestamp(weather_data["timestamp"])  # Convert UNIX timestamp to UTC
    ))

    # Process in batches of 5 records
    if len(data_list) >= 5:
        df = spark.createDataFrame(data_list, ["city", "temperature_c", "temperature_f", "humidity", "weather", "timestamp_utc"])
        
        # Transform timestamps
        df = df.withColumn("timestamp_utc", from_unixtime(col("timestamp_utc").cast("long")))

        # Save data to PostgreSQL
        df.write \
          .format("jdbc") \
          .option("url", f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}") \
          .option("dbtable", "weather") \
          .option("user", DB_USER) \
          .option("password", DB_PASSWORD) \
          .mode("append") \
          .save()
        
        print("✅ Data batch inserted into PostgreSQL using Spark!")
        data_list.clear()  # Clear batch

