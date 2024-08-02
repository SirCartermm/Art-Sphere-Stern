from flask import Blueprint
from flask_restful import Resource,Api,reqparse




artist_bp=Blueprint('artist',__name__,url_prefix='/artists')


def get_artwork(self,id):
    artwork = Artwork.query.get_or_404(id)
    return jsonify(ArtworkSchema().dump(artwork))


def put(self,id):
    artwork = Artwork.query.get_or_404(id)
    data = request.json
    
    artwork.title = data.get('title', artwork.title)
    artwork.description = data.get('description', artwork.description)
    artwork.image_url = data.get('image_url', artwork.image_url)
    artwork.price = data.get('price', artwork.price)
    artwork.genre = data.get('genre', artwork.genre)
    
    db.session.commit()
    
    return jsonify(ArtworkSchema().dump(artwork))

# Delete an Artwork
@app.route('/artworks/<int:id>', methods=['DELETE'])
def delete(self,id):
    artwork = Artwork.query.get_or_404(id)
    db.session.delete(artwork)
    db.session.commit()
    
    return jsonify({'message': 'Artwork deleted'}), 204