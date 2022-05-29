from flask import Response
from flask_restful import Resource
from models import Story
from views import get_authorized_user_ids
import json

# imported
from views import get_authorized_user_ids
import flask_jwt_extended

class StoriesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # get stories created by one of these users:
        # print(get_authorized_user_ids(self.current_user))

        user_ids = get_authorized_user_ids(self.current_user)
        listOfStories = []
        for user in user_ids:
            placeholder = Story.query.filter_by(user_id = user)
            for p in placeholder:
                listOfStories.append(p.to_dict())
        return Response(json.dumps(listOfStories), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        StoriesListEndpoint, 
        '/api/stories', 
        '/api/stories/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
