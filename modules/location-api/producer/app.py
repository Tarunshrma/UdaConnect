import json
import logging
import os


from kafka import KafkaProducer
from flask import Flask, jsonify, request, Response
from flask_restx import Namespace
from flask_accepts import accepts, responds
from schema import LocationSchema

app = Flask(__name__)
api = Namespace("udaconnect.location", description="udaconnect location api")  # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-api")

TOPIC_NAME = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER_URL"]


kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

# @app.before_request
# def before_request():
#     # Set up a Kafka producer


@api.route("/health")
def health():
    return jsonify({'response': 'Healthy'})


@api.route('/api/v1/locations', methods=['POST'])
@accepts(schema=LocationSchema)
@api.response(201, 'Location Created')
@api.response(400, 'Invalid Location Data')
def locations():
    request_body = request.json
    kafka_data = json.dumps(request_body).encode()
    kafka_producer.send(TOPIC_NAME, kafka_data)
    kafka_producer.flush()

    logger.info(
        f"location data to be submitted: {request_body}")

    return Response(status=201)


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
