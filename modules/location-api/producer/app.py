import json
import logging

from kafka import KafkaProducer
from flask import Flask, jsonify, request, Response


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-api")

TOPIC_NAME = 'location'
KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'
kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

# @app.before_request
# def before_request():
#     # Set up a Kafka producer


@app.route('/health')
def health():
    return jsonify({'response': 'Healthy'})


@app.route('/api/v1/locations', methods=['POST'])
def locations():
    request_body = request.json
    kafka_data = json.dumps(request_body).encode()
    kafka_producer.send(TOPIC_NAME, kafka_data)
    kafka_producer.flush()

    logger.info(
        f"location data to be submitted: {request_body}")

    return Response(status=202)


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
