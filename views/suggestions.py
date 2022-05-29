from flask import Response, request
from flask_restful import Resource
from models import User
from views import get_authorized_user_ids
import json

# imported
import random
import flask_jwt_extended

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # suggestions should be any user with an ID that's not in this list:
        # print(get_authorized_user_ids(self.current_user))

        all_user_ids = User.query.filter_by()
        user_ids = get_authorized_user_ids(self.current_user)

        notFollowed = []

        for u in all_user_ids:
            if u.id not in user_ids:
                notFollowed.append(u.to_dict())

        onlyseven = []

        for i in range(7):
            placeholder = notFollowed[random.randint(0, len(notFollowed)-1)]
            onlyseven.append(placeholder)
            notFollowed.remove(placeholder)

        return Response(json.dumps(onlyseven), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
