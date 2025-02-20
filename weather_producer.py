import json
import time
import requests
from kafka import KafkaProducer

# API Configuration
API_KEY = "d7a6bd635cbc04effccf9dab3dbd2783"
CITY = "Boston"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Kafka Configuration
KAFKA_TOPIC = "weather_data"
KAFKA_SERVER = "localhost:9092"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "timestamp": data["dt"]
        }
        return weather_info
    return None

if __name__ == "__main__":
    while True:
        weather_data = fetch_weather_data()
        if weather_data:
            print(f"Sending data: {weather_data}")
            producer.send(KAFKA_TOPIC, value=weather_data)
        time.sleep(10)  # Fetch weather data every 10 seconds
