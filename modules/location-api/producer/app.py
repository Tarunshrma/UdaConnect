import json
import logging
import os


from kafka import KafkaProducer
from flask import Flask, jsonify, request, Response
from flask_restx import Resource, Api, Namespace, reqparse
from flask_accepts import accepts, responds
from schema import LocationSchema

app = Flask(__name__)
api = Api(app, title="UdaConnect Location API")

namespace = Namespace("udaconnect.location", description="udaconnect location api")  # noqa
api.add_namespace(namespace, path=f"/api/v1/")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-api")

TOPIC_NAME = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER_URL"]


kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


@api.route('/api/v1/health')
class HealthResource(Resource):
    def get(self):
        return jsonify({'response': 'Healthy'})


parser = reqparse.RequestParser()
parser.add_argument('person_id', type=int, help='1', required=True)
parser.add_argument('creation_time', type=str,
                    help='2020-07-07T10:37:06', required=True)
parser.add_argument('latitude', type=str,
                    help='-122.290883', required=True)
parser.add_argument('longitude', type=str,
                    help='37.55363', required=True)


@api.doc(parser=parser)
@api.route('/api/v1/locations')
class LocationsResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(201, 'Location Created')
    @responds(400, 'Invalid Location Data')
    def post(self):
        request_body = request.json
        kafka_data = json.dumps(request_body).encode()
        kafka_producer.send(TOPIC_NAME, kafka_data)
        kafka_producer.flush()

        logger.info(
            f"location data to be submitted: {request_body}")

        return Response(status=201)


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
