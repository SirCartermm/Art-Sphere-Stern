from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from app.models import Artwork, db
from app.schemas import ArtworkSchema  # Assuming you have a schema for serializing/deserializing Artwork

artist_bp = Blueprint('artist', __name__, url_prefix='/artists')
api = Api(artist_bp)

class ArtworkResource(Resource):
    def get(self, id):
        artwork = Artwork.query.get_or_404(id)
        return ArtworkSchema().dump(artwork), 200

    def put(self, id):
        artwork = Artwork.query.get_or_404(id)
        data = request.get_json()

        artwork.title = data.get('title', artwork.title)
        artwork.description = data.get('description', artwork.description)
        artwork.image_url = data.get('image_url', artwork.image_url)
        artwork.price = data.get('price', artwork.price)
        artwork.genre = data.get('genre', artwork.genre)

        db.session.commit()

        return ArtworkSchema().dump(artwork), 200

    def delete(self, id):
        artwork = Artwork.query.get_or_404(id)
        db.session.delete(artwork)
        db.session.commit()

        return {'message': 'Artwork deleted'}, 204

# Add resource to API
api.add_resource(ArtworkResource, '/<int:id>')
