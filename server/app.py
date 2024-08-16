
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime
from flask_restful import Api, Resource
from config import DevelopmentConfig, ProductionConfig
from models import User, Artist, Artwork, Exhibition, ArtworkExhibition, Favorite, init_app, db

app = Flask(__name__)
CORS(app)

# Configuration setup (development or production)
app.config.from_object(DevelopmentConfig)
init_app(app)

bcrypt = Bcrypt()
jwt = JWTManager(app)
api = Api(app)

# Define Resources

class Register(Resource):
    def post(self):
        data = request.get_json()
        role = data.get('role', '').lower()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user = User(email=data['email'], password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()

        if role == 'artist':
            try:
                birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Invalid birthdate format. Use YYYY-MM-DD.'}), 400

            artist = Artist(
                name=data['name'],
                biography=data['biography'],
                birthdate=birthdate,
                nationality=data['nationality'],
                image=data.get('image', ''),
                user_id=user.id
            )

            db.session.add(artist)
            db.session.commit()

        return jsonify({'message': 'User created successfully'})

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict(),
                'role': user.role
            }, 200  # Return data and status code
        else:
            return {'message': 'Invalid email or password'}, 401 

class Logout(Resource):
    @jwt_required()
    def post(self):
        return jsonify({'message': 'Logout successful'})


class Dashboard(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return jsonify({'message': 'Welcome to your dashboard', 'user': user.to_dict()})


class ArtworkList(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        artwork = Artwork(
            title=data['title'],
            medium=data['medium'],
            style=data['style'],
            price=data['price'],
            available=data['available'],
            artist_id=get_jwt_identity()
        )
        db.session.add(artwork)
        db.session.commit()
        return jsonify({'message': 'Artwork created successfully'})

    def get(self):
        artworks = Artwork.query.all()
        return jsonify([artwork.to_dict() for artwork in artworks])


class ArtworkDetail(Resource):
    def get(self, id):
        artwork = Artwork.query.get_or_404(id)
        return jsonify(artwork.to_dict())

    @jwt_required()
    def put(self, id):
        artwork = Artwork.query.get_or_404(id)
        data = request.get_json()
        artwork.title = data['title']
        artwork.medium = data['medium']
        artwork.style = data['style']
        artwork.price = data['price']
        artwork.available = data['available']
        db.session.commit()
        return jsonify({'message': 'Artwork updated successfully'})

    @jwt_required()
    def delete(self, id):
        artwork = Artwork.query.get_or_404(id)
        db.session.delete(artwork)
        db.session.commit()
        return jsonify({'message': 'Artwork deleted successfully'})


class ExhibitionList(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        exhibition = Exhibition(
            name=data['name'],
            start_date=start_date,
            end_date=end_date,
            description=data['description'],
            artist_id=get_jwt_identity()
        )
        db.session.add(exhibition)
        db.session.commit()
        return jsonify({'message': 'Exhibition created successfully'})

    def get(self):
        exhibitions = Exhibition.query.all()
        return jsonify([exhibition.to_dict() for exhibition in exhibitions])


class ExhibitionDetail(Resource):
    def get(self, id):
        exhibition = Exhibition.query.get_or_404(id)
        return jsonify(exhibition.to_dict())

    @jwt_required()
    def put(self, id):
        exhibition = Exhibition.query.get_or_404(id)
        data = request.get_json()
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        exhibition.name = data['name']
        exhibition.start_date = start_date
        exhibition.end_date = end_date
        exhibition.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Exhibition updated successfully'})

    @jwt_required()
    def delete(self, id):
        exhibition = Exhibition.query.get_or_404(id)
        db.session.delete(exhibition)
        db.session.commit()
        return jsonify({'message': 'Exhibition deleted successfully'})


class ArtworkExhibitionResource(Resource):
    @jwt_required()
    def post(self, exhibition_id, artwork_id):
        artwork_exhibition = ArtworkExhibition(exhibition_id=exhibition_id, artwork_id=artwork_id)
        db.session.add(artwork_exhibition)
        db.session.commit()
        return jsonify({'message': 'Artwork added to exhibition successfully'})

    @jwt_required()
    def delete(self, exhibition_id, artwork_id):
        artwork_exhibition = ArtworkExhibition.query.filter_by(exhibition_id=exhibition_id, artwork_id=artwork_id).first()
        db.session.delete(artwork_exhibition)
        db.session.commit()
        return jsonify({'message': 'Artwork removed from exhibition successfully'})


class ArtistList(Resource):
    def get(self):
        artists = Artist.query.all()
        return jsonify([artist.to_dict() for artist in artists])


class ArtistDetail(Resource):
    def get(self, id):
        artist = Artist.query.get_or_404(id)
        return jsonify(artist.to_dict())

    @jwt_required()
    def put(self, id):
        artist = Artist.query.get_or_404(id)
        data = request.get_json()
        try:
            if 'birthdate' in data:
                artist.birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
            artist.biography = data.get('biography', artist.biography)
            artist.nationality = data.get('nationality', artist.nationality)
            artist.image = data.get('image', artist.image)
            db.session.commit()
            return jsonify({'message': 'Artist updated successfully'})
        except ValueError:
            return jsonify({'message': 'Invalid birthdate format. Use YYYY-MM-DD.'}), 400

    @jwt_required()
    def delete(self, id):
        artist = Artist.query.get_or_404(id)
        user = User.query.get(artist.user_id)
        db.session.delete(artist)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Artist and associated user deleted successfully'})


# Register Resources with API
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Dashboard, '/dashboard')

api.add_resource(ArtworkList, '/artworks')
api.add_resource(ArtworkDetail, '/artworks/<int:id>')

api.add_resource(ExhibitionList, '/exhibitions')
api.add_resource(ExhibitionDetail, '/exhibitions/<int:id>')

api.add_resource(ArtworkExhibitionResource, '/exhibitions/<int:exhibition_id>/artworks/<int:artwork_id>')

api.add_resource(ArtistList, '/artists')
api.add_resource(ArtistDetail, '/artists/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

