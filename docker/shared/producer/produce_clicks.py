import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# Kafka broker inside Docker network
producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

users = [f"user_{i}" for i in range(1, 501)]
pages = [
    "/", "/search", "/cart",
    "/category/mobiles", "/category/fashion", "/category/electronics"
]
products = [str(i) for i in range(100, 131)]
actions = ["view", "click", "add_to_cart", "checkout", "purchase"]

def make_event():
    page = random.choice(pages + [f"/product/{p}" for p in products])
    return {
        "user_id": random.choice(users),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "page": page,
        "action": random.choices(actions, weights=[60, 20, 10, 5, 5])[0],
    }

if __name__ == "__main__":
    print("Starting clickstream producer...")
    while True:
        event = make_event()
        producer.send("clickstream", event)
        print("Sent:", event)
        time.sleep(0.2)  # 5 events per second approx.
