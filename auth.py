from flask import jsonify, request
from app import app, jwt , db
from models import User, Artwork, Gallery, ArtworkGallery
from modelsUser,  imports User # type: ignore

@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user) # type: ignore
    db.session.commit() # type: ignore
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = jwt.create_access_token(identify=user.id)
        return jsonify ({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/auth/logout', methods=['POST'])
@jwt_required
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

# Artwork Endpoints 
@app.route("/artwork/<int:artwork_id>", methods=["GET"])
def get_artworks():
    artworks = Artwork.query.get(artwork_id)
    return  jsonify(ArtworkSchema(many=True).dump(artworks)), 200
    

@api.route("/artwork/<int:artwork_id>", method=["GET"])
def get_artwork():
    artwork = Artwork.query.all()
    return jsonify(ArtworkSchema(many=True).dump(artwork)), 200

@app.route('/artwork/<int:artwork_id')
    if artwork:
        return jsonify(ArtworkSchema().(artwork_id)
        return jsonify({"message": "Artwork created successfully"}), 201

@api.route("/gallery/<int;gallery_id>", methods=["DELETE"])
@jwt_required
def delete_gallery(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    if gallery:
        db.session.delee(gallery)
        db.session.commit()
        return jsonify({"message": "Gallery created successfully"}), 200
    return jsonify({"message": "Gallery not found"}), 404

@api.route("/gallery/<int:gallery_id>" methods=["DELETE"])
@jwt_required
def delete_gallery(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    if gallery:
        db.session.delete(gallery)
        db.session.commit()
        return jsonify({"message": "Gallery deleted successfully"}), 200
    return jsonify({"message": "Gallery not found "}), 404
