# 🌦️ Real-Time Weather Data Pipeline

## 📌 Project Overview
This project implements a **real-time data processing pipeline** that:
- **Extracts** weather data from an API.
- **Transforms** the data (converting temperatures and timestamps).
- **Loads** the processed data into PostgreSQL.
- **Streams** data using **Kafka** for real-time processing.

It is containerized using **Docker**, making deployment simple.

---

## 🛠️ Tech Stack
| Component       | Purpose |
|----------------|---------|
| **Apache Kafka**  | Message Broker for real-time streaming |
| **Zookeeper** | Manages Kafka Brokers |
| **PostgreSQL** | Stores processed weather data |
| **Python** | Fetches and processes the data |
| **Docker** | Manages all services |

---

## 🔧 Setup Instructions
To run this project, follow these steps:

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/real-time-weather-pipeline.git
cd real-time-weather-pipeline
2️⃣ Start the Services (Kafka, Zookeeper, PostgreSQL)
```
```bash
docker-compose up -d
```
This command starts Kafka, Zookeeper, and PostgreSQL in the background.

3️⃣ Run the Kafka Producer (Starts Streaming Data)
```bash
python weather_producer.py
```
Fetches weather data.
Sends it to Kafka in real time.
4️⃣ Run the Kafka Consumer (Processes and Stores Data)
```bash
python weather_consumer.py
```
Reads messages from Kafka.
Transforms and inserts them into PostgreSQL.
5️⃣ Check the Data in PostgreSQL
To verify that data is stored in the database:
```bash
docker exec -it postgres_db psql -U admin -d weather_db
```
Then, inside PostgreSQL, run:
```sql
SELECT * FROM weather LIMIT 10;
```
To exit:
```sql
\q
```
📸 Proof of Execution
✅ Running Containers
```bash
docker ps
```
✔️ Expected Output: Kafka, Zookeeper, and PostgreSQL should be running.

✅ Producer Sending Data
```bash
python weather_producer.py
```
✔️ Expected Output: Messages like:

```kotlin
Sending data: {'city': 'Boston', 'temperature': -8.37, 'humidity': 70, 'weather': 'overcast clouds', 'timestamp': 1740038005}
```
✅ Consumer Processing Data
```bash
python weather_consumer.py
```
✔️ Expected Output: Messages like:
```bash
Received: {'city': 'Boston', 'temperature': -8.37, 'humidity': 70, 'weather': 'overcast clouds', 'timestamp': 1740038005}
```
✅ Stored Data in PostgreSQL
```sql
SELECT * FROM weather LIMIT 10;
```
✔️ Expected Output: Rows with weather data.

🛑 How to Stop the Pipeline
To shut down everything, run:
```bash
docker-compose down
```
This stops and removes Kafka, Zookeeper, and PostgreSQL containers.

🔗 Additional Notes
If PostgreSQL doesn’t connect, check docker ps to ensure it’s running.
If Kafka doesn’t start, verify docker logs kafka.
If needed, restart the pipeline using:
```bash
docker-compose up -d
```
