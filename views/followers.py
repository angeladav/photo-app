from flask import Response, request
from flask_restful import Resource
from models import Following
import json

# imported
from views import get_authorized_user_ids
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        '''
        People who are following the current user.
        In other words, select user_id where following_id = current_user.id
        '''

        user_ids = get_authorized_user_ids(self.current_user)
        following = Following.query.filter_by(following_id = self.current_user.id)
        listOfFollowers = []
        for user in following:
            listOfFollowers.append(user.to_dict_follower())
        return Response(json.dumps(listOfFollowers), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
