from flask import Blueprint
from flask_restful import Resource,Api,reqparse


gallery_bp=Blueprint('gallery',__name__,url_prefix='/gallery')
class GalleryResource(Resource):
    def get(self, gallery_id):
        gallery = Gallery.query.get_or_404(gallery_id)
        return {
            'id': gallery.id,
            'name': gallery.name,
            'admin_id': gallery.admin_id
        }

    @jwt_required()
    def put(self, gallery_id):
        data = gallery_parser.parse_args()
        gallery = Gallery.query.get_or_404(gallery_id)
        gallery.name = data['name']
        gallery.admin_id = data['admin_id']
        db.session.commit()
        return {'message': 'Gallery updated successfully'}

    @jwt_required()
    def delete(self, gallery_id):
        gallery = Gallery.query.get_or_404(gallery_id)
        db.session.delete(gallery)
        db.session.commit()
        return {'message': 'Gallery deleted successfully'}

class GalleryListResource(Resource):
    def get(self):
        galleries = Gallery.query.all()
        return [{
            'id': gallery.id,
            'name': gallery.name,
            'admin_id': gallery.admin_id
        } for gallery in galleries]

    def post(self):
        data = gallery_parser.parse_args()
        new_gallery = Gallery(name=data['name'], admin_id=data['admin_id'])
        db.session.add(new_gallery)
        db.session.commit()
        return {'message': 'Gallery created successfully'}, 201

api.add_resource(GalleryResource, '/galleries/<int:gallery_id>')
api.add_resource(GalleryListResource, '/galleries')
