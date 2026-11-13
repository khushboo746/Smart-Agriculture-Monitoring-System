 
from confluent_kafka import Producer
import json
import random
import time
from datetime import datetime, timezone

# Connect Python to Kafka
producer = Producer({
    "bootstrap.servers": "localhost:9092"
})

TOPIC = "agriculture-sensor-data"


# Generate simulated sensor readings
def generate_sensor_data():

    data = {
        "farm_id": "FARM001",
        "sensor_id": "SENSOR01",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "soil_moisture": round(random.uniform(10, 80), 2),
        "temperature": round(random.uniform(20, 42), 2),
        "humidity": round(random.uniform(25, 90), 2)
    }

    return data


# Send data to Kafka
def delivery_report(err, msg):

    if err is not None:
        print("Message delivery failed:", err)

    else:
        print(
            f"Message sent to {msg.topic()} "
            f"[Partition {msg.partition()}]"
        )


print("🌱 Smart Agriculture Sensor Producer Started!")
print("Sending sensor data to Kafka every 3 seconds...\n")


try:
    while True:

        sensor_data = generate_sensor_data()

        producer.produce(
            TOPIC,
            key=sensor_data["sensor_id"],
            value=json.dumps(sensor_data),
            callback=delivery_report
        )

        producer.poll(0)

        print("\nSensor Reading:")
        print(json.dumps(sensor_data, indent=4))

        producer.flush()
        time.sleep(3)

except KeyboardInterrupt:
    print("\nProducer stopped.")

finally:
    producer.flush()
