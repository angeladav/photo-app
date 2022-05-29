from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json

# imported
from views import can_view_post
import flask_jwt_extended

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # get all bookmarks owned by the current user
        
        bookmarks = Bookmark.query.filter_by(user_id = self.current_user.id)
        listOfBookmarks = []
        for post in bookmarks:
            listOfBookmarks.append(post.to_dict())

        return Response(json.dumps(listOfBookmarks), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "bookmark" based on the data posted in the body 
        body = request.get_json()
        # print(body)

        if not body.get('post_id'):  
            return Response(json.dumps({"message": "post_id is required"}), mimetype="application/json", status=400)

        pid = body.get('post_id')
        
        if not isinstance(body.get('post_id'), int):
            if pid.isdigit():
                pid = int(pid)
            else:
                return Response(json.dumps({"message": "id={0} is invalid".format(body.get('post_id'))}), mimetype="application/json", status=400)

        listOfBookmarks = Bookmark.query.filter_by(user_id = self.current_user.id)

        for i in listOfBookmarks:

            if pid == i.post_id:
                
                return Response(json.dumps({"message": "already bookmarked post"}), mimetype="application/json", status=400)

        canBookmark = can_view_post(pid, self.current_user)

        if not canBookmark:
            return Response(json.dumps({"message": "id={0} is invalid".format(pid)}), mimetype="application/json", status=404)

        bookmark = Bookmark(user_id = self.current_user.id, post_id = pid)

        db.session.add(bookmark)
        db.session.commit()

        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "bookmark" record where "id"=id

        bm = Bookmark.query.get(id)

        if not bm:
            return Response(json.dumps({"message": "post was not bookmarked by user"}), mimetype="application/json", status=404)

        canBookmark = can_view_post(bm.post_id, self.current_user)

        if not canBookmark:
            return Response(json.dumps({"message": "id={0} is invalid".format(bm.post_id)}), mimetype="application/json", status=404)

        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()

        # print(id)
        return Response(json.dumps({"message": "id={0} was successfully deleted".format(id)}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
