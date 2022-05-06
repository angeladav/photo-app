import mimetypes
from flask import Response, request
from flask_restful import Resource
from models import Post, db
from views import get_authorized_user_ids

import json

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        args = request.args
        user_ids = get_authorized_user_ids(self.current_user)

        try:
            limit = int(args.get('limit') or 20)
        except:
            return Response(json.dumps({"message": "invalid limit parameter"}), mimetype="application/json", status=400)
        if limit > 50:
            return Response(json.dumps({"message": "limit too large"}), mimetype="application/json", status=400)

        posts = Post.query.filter(Post.user_id.in_(user_ids)).limit(limit)
        posts_json = [post.to_dict() for post in posts]
        return Response(json.dumps(posts_json), mimetype="application/json", status=200)

    def post(self):
        # create a new post based on the data posted in the body 
        body = request.get_json()

        if not body.get('image_url'):  
            return Response(json.dumps({"message": "image_url is required"}), mimetype="application/json", status=400)
        new_post = Post(image_url = body.get('image_url'), user_id = self.current_user.id, caption = body.get('caption'), alt_text = body.get('alt_text'))

        db.session.add(new_post)
        db.session.commit()

        return Response(json.dumps(new_post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        

    def patch(self, id):
        # update post based on the data posted in the body 
        
        body = request.get_json()
        post = Post.query.get(id)
        
        if not post:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        if self.current_user.id != post.user_id:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        user_ids = get_authorized_user_ids(self.current_user)
        if post.user_id not in user_ids or not post:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        updated_post = Post(image_url = body.get('image_url'), user_id = self.current_user.id, caption = body.get('caption'), alt_text = body.get('alt_text'))

        if (updated_post.image_url):
            post.image_url = updated_post.image_url
        if (updated_post.alt_text):
            post.alt_text = updated_post.alt_text
        if (updated_post.caption):
            post.caption = updated_post.caption
        
        db.session.commit()

        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)


    def delete(self, id):
        # delete post where "id"=id

        post = Post.query.get(id)
        if not post:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        if self.current_user.id != post.user_id:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        Post.query.filter_by(id=id).delete()
        db.session.commit()

        return Response(json.dumps({"message": "id={0} was successfully deleted".format(id)}), mimetype="application/json", status=200)


    def get(self, id):
        # get the post based on the id

        post = Post.query.get(id)
        if not post:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        if self.current_user.id != post.user_id:
            return Response(json.dumps({"message": "id={0} is invalid".format(id)}), mimetype="application/json", status=404)

        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )