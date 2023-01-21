import logging
from schema import LocationSchema
from models import Location
from typing import Dict
from geoalchemy2.functions import ST_AsText, ST_Point
from app import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-db-app")


class LocationDBService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        logger.info("TESTING>>>>>>>>>>")
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(
            location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location
