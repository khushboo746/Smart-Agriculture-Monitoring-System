# 🌱 Smart Agriculture Monitoring System

## Project Overview

The Smart Agriculture Monitoring System is an IoT-based project that monitors agricultural conditions using simulated sensor data, Apache Kafka and Apache Cassandra.

It collects soil moisture, temperature and air humidity readings, processes them in real time and stores them in a database. A Streamlit dashboard displays the readings through metrics, graphs and alerts.

## Technologies Used

- Python 3.10
- Apache Kafka
- Apache Cassandra
- Docker and Docker Compose
- Streamlit
- Pandas
- Plotly

## System Architecture

**Python Producer → Apache Kafka → Python Consumer → Apache Cassandra → Streamlit Dashboard**

### Working

1. **Producer:** Generates simulated agriculture sensor readings.
2. **Kafka:** Transfers sensor data through the `agriculture-sensor-data` topic.
3. **Consumer:** Receives readings, checks their status and processes them.
4. **Cassandra:** Stores the sensor readings in the `agriculture` keyspace.
5. **Dashboard:** Displays sensor values, alerts, graphs and historical records.

## Features

- Real-time sensor data processing
- Soil moisture monitoring
- Temperature monitoring
- Air humidity monitoring
- Dry soil and high-temperature alerts
- Sensor history graphs
- Automatic dashboard refresh
- CSV data download

## Project Structure

```text
Smart_Agriculture_Monitoring_System/
│
├── producer.py
├── consumer.py
├── dashboard.py
├── database.py
├── requirements.txt
├── docker-compose.yml
├── README.md
└── screenshots/
```

## Installation and Execution

### 1. Start Docker containers

```bash
docker compose up -d
```

### 2. Activate Python environment

```powershell
.\venv310\Scripts\Activate.ps1
```

### 3. Start the Producer

```bash
python producer.py
```

### 4. Start the Consumer

Open another terminal and activate the environment, then run:

```bash
python consumer.py
```

### 5. Start the Dashboard

Open another terminal, activate the environment and run:

```bash
python -m streamlit run dashboard.py
```

Open the dashboard at:

http://localhost:8501

## Database Details

- Database: Apache Cassandra
- Keyspace: `agriculture`
- Table: `sensor_readings`

## Alert Conditions

- Soil moisture below 30%: Dry Soil
- Temperature above 35°C: High Temperature
- Otherwise: Normal

*These are demonstration thresholds and should be adjusted according to crop requirements.*

## Conclusion

This project demonstrates how real-time data processing and distributed databases can be used in smart agriculture. It helps monitor environmental conditions and provides useful information for agricultural decision-making.

## Future Scope

- Integration with ESP32 and real physical sensors
- Automatic irrigation system
- Mobile application integration
- Crop-specific alert thresholds
- Weather forecasting integration

---
**Project:** Smart Agriculture Monitoring System  
**Technology:** Apache Kafka and Apache Cassandra  
**Category:** Internet of Things (IoT) and Big Data Analytics
Save these screenshots inside your screenshots folder:
