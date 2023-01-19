from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-api")


TOPIC_NAME = 'location'
KAFKA_SERVER = '146.190.34.54:30407'
kafka_consumer = KafkaConsumer(TOPIC_NAME,bootstrap_servers=KAFKA_SERVER)


while True:
    for location in kafka_consumer:
        message = location.value.decode('utf-8')
        location_message = json.loads(message)
        logger.info(
            f"location data recieved: {location_message}")