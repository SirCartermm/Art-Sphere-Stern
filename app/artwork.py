from flask import Blueprint, request, jsonify
from app.models import Artwork

bp = Blueprint('artwork', __name__, url_prefix='/artwork')

@bp.route('/', methods=['POST'])
def add_artwork():
    data = request.get_json()
    title = data['title']
    artist = data['artist']
    price = data['price']

    new_artwork = Artwork(title=title, artist=artist, price=price)
    db.session.add(new_artwork)
    db.session.commit()

    return jsonify({'message': 'Artwork added successfully'}), 201

@bp.route('/', methods=['GET'])
def list_artworks():
    artworks = Artwork.query.all()
    return jsonify([{'id': a.id, 'title': a.title, 'artist': a.artist, 'price': a.price} for a in artworks]), 200
