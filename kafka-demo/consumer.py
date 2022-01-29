import json
from kafka import KafkaConsumer

if __name__=="__main__":

    consumer=KafkaConsumer(
        "demo",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest"
    )

    for msg in consumer:
        print(json.loads(msg.value))
