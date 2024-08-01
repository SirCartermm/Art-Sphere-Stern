from app import app, db, ma, jwt
from models import User, Artwork, Gallery

@app.route('/galleries', methods=['GET'])
def get_galleries():
    galleries = Gallery.query.all()
    return jsonify([gallery.to_dict() for gallery in galleries]), 200


@app.route('/artwork/<int:id>', methods =['GET'])
def get_artwork(id):
    artwork = Artwork.query.get(id)
    if artwork:
        return jsonify(artwork.to_dict()), 200
    return jsonify({'message': 'Artwork not found'}), 404
