from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import enum

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
ma = Marshmallow()
jwt = JWTManager()

# Enum for user roles
class Role(enum.Enum):
    artist = 'artist'
    viewer = 'viewer'
    admin = 'admin'

# Define the models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)

    artworks = db.relationship('Artwork', backref='artist', lazy=True)
    galleries = db.relationship('Gallery', backref='admin', lazy=True)

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    genre = db.Column(db.String(100), nullable=True)

    artist = db.relationship('User', backref=db.backref('artworks', lazy=True))
    galleries = db.relationship('Gallery', secondary='artwork_gallery', backref='artworks')

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    admin = db.relationship('User', backref=db.backref('galleries', lazy=True))
    artworks = db.relationship('Artwork', secondary='artwork_gallery', backref='galleries')

class ArtworkGallery(db.Model):
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), primary_key=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), primary_key=True)

    artwork = db.relationship('Artwork', backref=db.backref('artwork_galleries'))
    gallery = db.relationship('Gallery', backref=db.backref('artwork_galleries'))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Define schemas
class ArtworkSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Artwork
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class GallerySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Gallery
        load_instance = True

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True

# Define Blueprints and Resources
api_bp = Blueprint('api', __name__)

# Auth Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password, role=Role.viewer.value)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Artwork Blueprint
artwork_bp = Blueprint('artwork', __name__, url_prefix='/artworks')
api = Api(artwork_bp)

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

api.add_resource(ArtworkResource, '/<int:id>')

# Gallery Blueprint
gallery_bp = Blueprint('gallery', __name__, url_prefix='/galleries')
api = Api(gallery_bp)

class GalleryResource(Resource):
    def get(self, gallery_id):
        gallery = Gallery.query.get_or_404(gallery_id)
        return GallerySchema().dump(gallery), 200

    @jwt_required()
    def put(self, gallery_id):
        data = request.get_json()
        gallery = Gallery.query.get_or_404(gallery_id)
        gallery.name = data.get('name', gallery.name)
        gallery.admin_id = data.get('admin_id', gallery.admin_id)
        db.session.commit()
        return {'message': 'Gallery updated successfully'}, 200

    @jwt_required()
    def delete(self, gallery_id):
        gallery = Gallery.query.get_or_404(gallery_id)
        db.session.delete(gallery)
        db.session.commit()
        return {'message': 'Gallery deleted successfully'}, 204

class GalleryListResource(Resource):
    def get(self):
        galleries = Gallery.query.all()
        return GallerySchema(many=True).dump(galleries), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_gallery = Gallery(name=data['name'], admin_id=data['admin_id'])
        db.session.add(new_gallery)
        db.session.commit()
        return {'message': 'Gallery created successfully'}, 201

api.add_resource(GalleryResource, '/<int:gallery_id>')
api.add_resource(GalleryListResource, '/')

# Order Blueprint
order_bp = Blueprint('order', __name__, url_prefix='/orders')
@order_bp.route('/', methods=['POST'])
def place_order():
    data = request.get_json()
    user_id = data['user_id']
    artwork_id = data['artwork_id']
    quantity = data['quantity']

    new_order = Order(user_id=user_id, artwork_id=artwork_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'}), 201

@order_bp.route('/', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return jsonify(OrderSchema(many=True).dump(orders)), 200

# Create the Flask app
def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(artwork_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(order_bp)

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)



