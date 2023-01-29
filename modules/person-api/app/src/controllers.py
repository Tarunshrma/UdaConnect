from app.src.models import Person
from app.src.schemas import PersonSchema
from app.src.services import PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, reqparse
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("udaconnect.person", description="udaconnect person api")  # noqa

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='Tarun', required=True)
parser.add_argument('last_name', type=str,
                    help='Sharma', required=True)
parser.add_argument('company_name', type=str,
                    help='ABC Company', required=True)


@api.doc(parser=parser)
@api.route("/v1/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/v1/persons/<person_id>")
@api.param("person_id", "Fetch person from id", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person
