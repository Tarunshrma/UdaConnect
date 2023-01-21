from kafka import KafkaConsumer
import json
import logging

import grpc
import location_data_pb2
import location_data_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-api")


TOPIC_NAME = 'location'
KAFKA_SERVER = 'my-release-kafka.default.svc.cluster.local:9092'
DB_SERVICE_URL = "location-db-service:5005"
kafka_consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)


def send_to_location_db_service(location_message):
    print("Sending location data to db grpc service")
    channel = grpc.insecure_channel(DB_SERVICE_URL)
    stub = location_data_pb2_grpc.LocationServiceStub(channel)

    item = location_data_pb2.LocationData(
        person_id=location_message["person_id"],
        creation_time=location_message["creation_time"],
        latitude=location_message["latitude"],
        longitude=location_message["longitude"],
    )
    response = stub.SaveLocation(item)


while True:
    for location in kafka_consumer:
        message = location.value.decode('utf-8')
        location_message = json.loads(message)
        logger.info(
            f"location data recieved: {location_message}")
        send_to_location_db_service(location_message)
