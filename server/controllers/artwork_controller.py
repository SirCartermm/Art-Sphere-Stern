from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///artwork.db"
db = SQLAlchemy(app)

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description =db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Artwork('{self.title}', '{self.description}', '{self.price}', '{self.image}', '{self.artist}')"
    
class ArtworkController:
    def get_all_artworks(self):
        artworks = Artworks.query.all()
        return jsonify([artwork.to_dict() for artwork in artworks])
    
    def get_artwork_by_id(self, id):
        artwork = Artwork.query.get(id)
        if artwork is None:
            return jsonify({"error": "Artwork not found"}), 404
        return jsonify(artwork.to_dict())
    
    def create_artwork(self):
        data = request.get_json()
        artwork = Artwork(title=data["title"], description=data["description"], price=data["price"], image=data["image"], artist=data["artist"])
        db.session.add(artwork)
        db.session.commit()
        return jsonify(artwork.to_dict())
    
    def update_artwork(self, id):
        artwork = Artwork.query.get(id)
        if artwork is None:
            return jsonify({"error": "Artwork not found"}), 404
        data = request.get_json()
        artwork.title = data["title"]
        artwork.description = data["description"]
        artwork.price = data["price"]
        artwork.image = data["image"]
        artwork.artist = data["artist"]
        db.session.commit()
        return jsonify(artwork.to_dict())
    def delete_artwork(self, id):
        artwork = Artwork.query.get(id)
        if artwork is None:
            return jsonify({"error": "Artwork not found"}), 404
        db.session.delete(artwork)
        db.session.commit()
        return jsonify({"message": "Artwork deleted"})
    
    @app.route("/artwork", methods=["GET"])
    def get_all_artworks():
        return ArtworkController().get_artworks_by_id(id)
    
    @app.route("/artworks/<int:id>", methods=["GET"])
    def get_artwork_by_id(id):
        return ArtworkController().get_artwork_by_id(id)
    
    @app.route("/artworks", methods=["POST"])
    def create_artwork():
        return ArtworkController().create_artworks()
    
    @app.route("/artworks/<int:id>", methods=["PUT"])
    def update_artwork(id):
        return ArtworkController().update_artwork(id)
    
    @app.route("/artworks/<int:id>", methods=["DELETE"])
    def delete_artwork(id):
        return ArtworkController().delete_artwork(id)
    

    if __name__ == "__main__":
        app.run(debug=True)
        