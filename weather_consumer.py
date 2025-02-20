import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime

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

for message in consumer:
    weather_data = message.value
    print(f"Received: {weather_data}")

    # **Transformations**
    temperature_c = weather_data["temperature"]
    temperature_f = (temperature_c * 9/5) + 32  # Convert °C to °F
    timestamp_utc = datetime.utcfromtimestamp(weather_data["timestamp"])  # Convert to UTC timestamp

    # Insert transformed data into PostgreSQL
    cursor.execute("""
        INSERT INTO weather (city, temperature_c, temperature_f, humidity, weather, timestamp_utc)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (weather_data["city"], temperature_c, temperature_f, weather_data["humidity"], weather_data["weather"], timestamp_utc))

    conn.commit()
