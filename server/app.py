from flask import Flask, request
from flask_restful import Api, Resource # type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Artwork
from flask_cors import CORS # type: ignore
from models import db, Artwork

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artsphere.db'
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    CORS(app)

    # Resources
    class Artworks(Resource):
        def get(self, artwork_id=None):
            if artwork_id:
                artwork = Artwork.query.get_or_404(artwork_id)
                return artwork.to_dict()
            else:
                page = request.args.get('page', 1, type=int)
                per_page = request.args.get('per_page', 10, type=int)
                artworks = Artwork.query.paginate(page, per_page, False)
                return [artwork.to_dict() for artwork in artworks]

        def post(self):
            data = request.get_json()
            new_artwork = Artwork(**data)
            db.session.add(new_artwork)
            db.session.commit()
            return new_artwork.to_dict(), 201

        def put(self, artwork_id):
            artwork = Artwork.query.get_or_404(artwork_id)
            data = request.get_json()
            for key, value in data.items():
                setattr(artwork, key, value)
            db.session.commit()
            return artwork.to_dict()

        def delete(self, artwork_id):
            artwork = Artwork.query.get_or_404(artwork_id)
            db.session.delete(artwork)
            db.session.commit()
            return '', 204
        
    # Routes
    api.add_resource(Artworks, '/artworks', '/artworks/<int:artwork_id>')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
