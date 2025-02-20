# Real-Time Weather Data Processing Pipeline 🌦️

## 📌 Project Overview
This project builds a **real-time data pipeline** using:
- **Kafka** for streaming data.
- **PostgreSQL** for storing data.
- **Python** for processing and transforming weather data.
- **Docker** for containerization.

The pipeline **fetches weather data**, **transforms it**, and **stores it** in PostgreSQL for analysis.

---

## 🚀 Tech Stack
- **Apache Kafka** - Message Broker
- **PostgreSQL** - Database
- **Python** - Data Processing
- **Docker** - Containerization
- **Kafka-Python & Psycopg2** - Libraries

---

## 🔧 Setup Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/real-time-weather-pipeline.git
cd real-time-weather-pipeline
```
2️⃣ Start the Services (Kafka, Zookeeper, PostgreSQL)
```bash
docker-compose up -d
```
3️⃣ Run the Kafka Producer
```bash
python weather_producer.py
```
4️⃣ Run the Kafka Consumer
```bash
python weather_consumer.py
```
5️⃣ Check the Data in PostgreSQL
```bash
docker exec -it postgres_db psql -U admin -d weather_db
SELECT * FROM weather LIMIT 10;
\q  # Exit PostgreSQL
```
