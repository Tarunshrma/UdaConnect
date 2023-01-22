import time
from concurrent import futures

import grpc
import location_data_pb2
import location_data_pb2_grpc
import logging
from typing import Dict, List

# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, jsonify
# from config import LocationDBService
# from service import LocationDBService
# import config
from service import LocationDBService
from models import Location
from config import create_app
# db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-db-app")


class LocationServicer(location_data_pb2_grpc.LocationServiceServicer):
    def SaveLocation(self, request, context):

        request_value = {
            "person_id": int(request.person_id),
            "creation_time": request.creation_time,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }
        logger.info(f"Saving location data {request_value} to database")

        with app.app_context():
            db_response = LocationDBService.create(request_value)
            logger.info(f"Saved location data {db_response} to database")

        return location_data_pb2.LocationData(**request_value)

    def GetAllLocations(self, request, context):
        logger.info(f"Request recieved to get all the locations")
        result = location_data_pb2.LocationDataList()
        with app.app_context():
            locations: List[Location] = LocationDBService.retrieve_all()
            logger.info(f"Retrieved location data {locations} from database")
            items: List[location_data_pb2.LocationData] = []
            for loc in locations:
                item = location_data_pb2.LocationData(
                    person_id=loc.person_id,
                    creation_time=loc.creation_time,
                    latitude=loc.latitude,
                    longitude=loc.longitude,
                )

                items.append(item)

            result.locations.extend(item)
            return result

            # Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_data_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationServicer(), server)


logger.info("Location db service starting on port 5005...")
server.add_insecure_port("[::]:5005")
app = create_app()
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
