from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json

# imported
from views import get_authorized_user_ids 
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # return all of the "following" records that the current user is following

        user_ids = get_authorized_user_ids(self.current_user)
        following = Following.query.filter_by(follower = self.current_user)
        listOfFollowers = []
        for user in following:
            listOfFollowers.append(user.to_dict_following())
        return Response(json.dumps(listOfFollowers), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "following" record based on the data posted in the body 
        k = []
        body = request.get_json()

        if not body.get('user_id'):
            return Response(json.dumps({"message": "following_id is required"}), mimetype="application/json", status=400)

        uid = body.get('user_id')
        if not isinstance(uid, int):
            if uid.isdigit():
                uid = int(uid)
            else:
                return Response(json.dumps({"message": "id={0} is invalid".format(uid)}), mimetype="application/json", status=400)

        user_ids = User.query.get(uid)

        if not user_ids:
            return Response(json.dumps({"message": "id={0} is invalid".format(uid)}), mimetype="application/json", status=404)

        followingOrNot  = Following.query.filter_by(user_id = self.current_user.id)

        for person in followingOrNot:
            if person.following_id == uid:
                return Response(json.dumps({"message": "already following user"}), mimetype="application/json", status=400)
        
        follow = Following(user_id = self.current_user.id, following_id = uid)

        db.session.add(follow)
        db.session.commit()

        return Response(json.dumps(follow.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "following" record where "id"=id
        
        follow = Following.query.get(id)

        if not follow:
            return Response(json.dumps({"message": "post was not bookmarked by user"}), mimetype="application/json", status=404)

        if follow.user_id != self.current_user.id:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        Following.query.filter_by(id=id).delete()
        db.session.commit()

        print(id)
        return Response(json.dumps({}), mimetype="application/json", status=200)




def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
