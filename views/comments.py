from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post

# imported
from views import can_view_post
import flask_jwt_extended

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "Comment" based on the data posted in the body 
        body = request.get_json()

        if not isinstance(body.get('post_id'), int):
            return Response(json.dumps({"message": "id={0} is invalid".format(body.get('post_id'))}), mimetype="application/json", status=400)

        if not body.get('text') or not body.get('post_id'):
            return Response(json.dumps({"message": "both text and post_id is required"}), mimetype="application/json", status=400)

        canComment = can_view_post(body.get('post_id'), self.current_user)

        if not canComment:
            return Response(json.dumps({"message": "id={0} is invalid".format(body.get('post_id'))}), mimetype="application/json", status=404)

        comment = Comment(text = body.get('text'), user_id = self.current_user.id, post_id = body.get('post_id'))

        db.session.add(comment)
        db.session.commit()

        # print(body)
        return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "Comment" record where "id"=id
        # print(id)

        cm = Comment.query.get(id)

        if not cm:
            return Response(json.dumps({"message": "post was not bookmarked by user"}), mimetype="application/json", status=404)

        if cm.user_id != self.current_user.id:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        Comment.query.filter_by(id=id).delete()
        db.session.commit()

        return Response(json.dumps({"message": "id={0} was successfully deleted".format(id)}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
