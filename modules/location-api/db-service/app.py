import time
from concurrent import futures

import grpc
import location_data_pb2
import location_data_pb2_grpc
import logging

# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, jsonify
from config import create_app

# db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-db-app")


class LocationServicer(location_data_pb2_grpc.LocationServiceServicer):
    def SaveLocation(self, request, context):
        from service import LocationDBService

        request_value = {
            "person_id": int(request.person_id),
            "creation_time": request.creation_time,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }
        logger.info(f"Saving location data {request_value} to database")
        LocationDBService.create(request_value)

        return location_data_pb2.LocationData(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_data_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationServicer(), server)


logger.info("Location db service starting on port 5005...")
server.add_insecure_port("[::]:5005")
create_app()
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
