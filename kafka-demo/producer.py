import time,json,random
from datetime import datetime
from data_generator import generate_message
from kafka import KafkaProducer


def serializer(message):
    return json.dumps(message).encode("utf-8")


producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=serializer
)

if __name__=="__main__":

    while True:

        dummy_messages=generate_message()

        print(f"Producing message {datetime.now()} | Message = {str(dummy_messages)}")
        producer.send("demo",dummy_messages)

        time.sleep(2)

