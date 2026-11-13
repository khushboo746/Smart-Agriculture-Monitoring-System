
from cassandra.io.asyncorereactor import AsyncoreConnection
from confluent_kafka import Consumer
from cassandra.cluster import Cluster
from datetime import datetime
import json

# 1. Connect to Kafka
consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "agriculture-group",
    "auto.offset.reset": "earliest"
})

TOPIC = "agriculture-sensor-data"

# 2. Connect to Cassandra
cluster = Cluster(
    ["127.0.0.1"],
    connection_class=AsyncoreConnection
)
session = cluster.connect("agriculture")

# 3. Prepare Cassandra insert query
insert_query = session.prepare("""
    INSERT INTO sensor_readings (
        farm_id,
        reading_date,
        event_time,
        sensor_id,
        soil_moisture,
        temperature,
        humidity,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""")

# 4. Subscribe to Kafka topic
consumer.subscribe([TOPIC])

print("🌱 Agriculture Kafka Consumer Started!")
print("Waiting for sensor readings...\n")


try:
    while True:

        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Kafka error:", msg.error())
            continue

        # Read JSON message
        data = json.loads(msg.value().decode("utf-8"))

        # Convert timestamp
        event_time = datetime.fromisoformat(
            data["timestamp"].replace("Z", "+00:00")
        ).replace(tzinfo=None)

        reading_date = event_time.date()

        soil = float(data["soil_moisture"])
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])

        # Check sensor conditions
        if soil < 30:
            status = "Dry Soil"
        elif temperature > 35:
            status = "High Temperature"
        else:
            status = "Normal"

        # Save reading in Cassandra
        session.execute(
            insert_query,
            (
                data["farm_id"],
                reading_date,
                event_time,
                data["sensor_id"],
                soil,
                temperature,
                humidity,
                status
            )
        )

        print("Reading saved successfully!")
        print("Farm:", data["farm_id"])
        print("Soil Moisture:", soil, "%")
        print("Temperature:", temperature, "°C")
        print("Humidity:", humidity, "%")
        print("Status:", status)
        print("-" * 40)


except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
    cluster.shutdown()
    
