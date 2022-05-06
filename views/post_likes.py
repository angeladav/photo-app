from asyncio.windows_events import NULL
from flask import Response, request
from flask_restful import Resource
from models import LikePost, db
import json

# imported
from models import Post, db
from views import can_view_post

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "like_post" based on the data posted in the body 
        body = request.get_json()

        if not isinstance(body.get('post_id'), int):
            return Response(json.dumps({"message": "id={0} is invalid".format(body.get('post_id'))}), mimetype="application/json", status=400)

        if not body.get('post_id'):  
            return Response(json.dumps({"message": "post_id is required"}), mimetype="application/json", status=400)

        post = Post.query.get(body.get('post_id'))
        canLike = can_view_post(body.get('post_id'), self.current_user)

        if not post or not canLike:
            return Response(json.dumps({"message": "id={0} is invalid".format(body.get('post_id'))}), mimetype="application/json", status=404)

        listOfLikes = LikePost.query.filter(LikePost.post_id.in_((body.get('post_id'), self.current_user.id)))

        for i in listOfLikes:

            if self.current_user.id == i.user_id:
                
                return Response(json.dumps({"message": "already liked post"}), mimetype="application/json", status=400)

        new_like = LikePost(user_id = self.current_user.id, post_id = body.get('post_id'))

        db.session.add(new_like)
        db.session.commit()
        
        return Response(json.dumps(new_like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "like_post" where "id"=id

        if not isinstance(id, int):
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=400)

        if id == NULL:  
            return Response(json.dumps({"message": "post_id is required"}), mimetype="application/json", status=400)

        post_like = LikePost.query.get(id)

        if not post_like:
            return Response(json.dumps({"message": "post was not liked by user"}), mimetype="application/json", status=404)

        canLike = can_view_post(post_like.post_id, self.current_user)

        if not canLike:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()

        return Response(json.dumps({"message": "id={0} was successfully deleted".format(id)}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
