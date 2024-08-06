from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from config import app, db, login_manager
from models import Artwork, Category, User, Payment, ArtistArtwork, UserRequest, Artist, Transaction
from datetime import datetime

api = Api(app)

class Index(Resource):
    def get(self):
        return '<h1>WELCOME !!</h1>'


class SignUp(Resource):
    def post(self):
        data = request.get_json()

        # Validate incoming data
        if not data or not isinstance(data, dict):
            return {"error": "Invalid JSON data"}, 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'User').capitalize()  # Default role is 'User'

        # Validate required fields
        if not name or not email or not password:
            return {"error": "All fields are required"}, 422

        # Validate role
        if role not in ['Admin', 'User']:
            return {"error": "Invalid role"}, 422

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user object
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            # Provide appropriate success message based on role
            message = "Admin created successfully" if role == 'Admin' else "User created successfully"
            return {"message": message}, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Email already exists"}, 422
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to create user", "details": str(e)}, 500
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'success': False, 'message': 'Email and password are required'}, 400

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return {'success': False, 'message': 'Invalid email or password'}, 401

        login_user(user)
        return {'success': True, 'message': 'Login successful'}

class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {"message": "Logged out successfully"}, 200

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return user.to_dict(), 200
            else:
                return {"error": "User not found"}, 404
        else:
            return {"error": "Unauthorized"}, 401

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users]

class ManageUser(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict()

    def patch(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()
        role = data.get('role')

        if role is not None:
            user.role = role
            try:
                db.session.commit()
                return user.to_dict(), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500

        return {"error": "Invalid data"}, 400

class UserDetails(Resource):
    @login_required
    def get(self):
        user_id = current_user.id
        user = User.query.get(user_id)
        return make_response(user.to_dict(), 200)

class Profile(Resource):
    @login_required
    def get(self):
        user = current_user
        transactions = Transaction.query.filter_by(user_id=user.id).all()
        transaction_history = [transaction.to_dict() for transaction in transactions]
        activities = get_user_activities(user.id)

        user_profile = {
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at,
            'transaction_history': transaction_history,
            'activities': activities
        }

        return user_profile, 200

def get_user_activities(user_id):
    activities = [
        {'activity': 'Logged in', 'timestamp': datetime.utcnow()},
        {'activity': 'Made a purchase', 'timestamp': datetime.utcnow()},
    ]
    return activities

class ArtworkList(Resource):
    def get(self):
        artworks = Artwork.query.all()
        return [artwork.to_dict() for artwork in artworks]

class ArtworkDetail(Resource):
    def get(self, artwork_id):
        artwork = Artwork.query.get(artwork_id)
        if not artwork:
            return {'error': 'Artwork not found'}, 404
        return artwork.to_dict()

    def put(self, artwork_id):
        artwork = Artwork.query.get(artwork_id)
        if not artwork:
            return {'error': 'Artwork not found'}, 404

        data = request.get_json()
        name = data.get('name')
        category_id = data.get('category_id')
        bp = data.get('bp')
        sp = data.get('sp')

        if name is not None:
            artwork.name = name
        if category_id is not None:
            artwork.category_id = category_id
        if bp is not None:
            artwork.bp = bp
        if sp is not None:
            artwork.sp = sp

        try:
            db.session.commit()
            return artwork.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, artwork_id):
        artwork = Artwork.query.get(artwork_id)
        if not artwork:
            return {'error': 'Artwork not found'}, 404

        try:
            db.session.delete(artwork)
            db.session.commit()
            return {'message': 'Artwork deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class CreateArtwork(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        category_id = data.get('category_id')
        bp = data.get('bp')
        sp = data.get('sp')

        if not all([name, category_id, bp, sp]):
            return {'error': 'Missing data'}, 400

        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}, 404

        new_artwork = Artwork(
            name=name,
            category_id=category_id,
            bp=bp,
            sp=sp
        )

        try:
            db.session.add(new_artwork)
            db.session.commit()
            return new_artwork.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class PaymentList(Resource):
    def get(self):
        payments = Payment.query.all()
        return [payment.to_dict() for payment in payments]

    def post(self):
        data = request.get_json()
        inventory_id = data.get('inventory_id')
        amount = data.get('amount')
        payment_date_str = data.get('payment_date')

        if inventory_id is None:
            return {'error': 'Missing inventory_id'}, 400
        if amount is None:
            return {'error': 'Missing amount'}, 400
        if payment_date_str is None:
            return {'error': 'Missing payment_date'}, 400

        try:
            payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d')
        except ValueError:
            return {'error': 'Invalid payment_date format'}, 400

        try:
            amount = float(amount)
        except ValueError:
            return {'error': 'Invalid amount format'}, 400

        payment = Payment(
            inventory_id=inventory_id,
            amount=amount,
            payment_date=payment_date
        )
        try:
            db.session.add(payment)
            db.session.commit()
            return {'message': 'Payment made successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class CategoryList(Resource):
    def get(self):
        categories = Category.query.all()
        return [category.to_dict() for category in categories]

class ArtworksByCategory(Resource):
    def get(self, category_id):
        artworks = Artwork.query.filter_by(category_id=category_id).all()
        return [artwork.to_dict() for artwork in artworks]

class ArtistList(Resource):
    def get(self):
        artists = Artist.query.all()
        return [artist.to_dict() for artist in artists]

class ArtistArtworkList(Resource):
    def get(self):
        artist_artworks = ArtistArtwork.query.all()
        return [artist_artwork.to_dict() for artist_artwork in artist_artworks]

    def post(self):
        data = request.get_json()
        artwork_id = data.get('artwork_id')
        artist_id = data.get('artist_id')
        price = data.get('price')

        if not all([artwork_id, artist_id, price]):
            return {'error': 'Missing data'}, 400

        artist_artwork = ArtistArtwork(
            artwork_id=artwork_id,
            artist_id=artist_id,
            price=price
        )

        try:
            db.session.add(artist_artwork)
            db.session.commit()
            return artist_artwork.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class UserRequestList(Resource):
    def get(self):
        supply_requests = UserRequest.query.all()
        return [supply_request.to_dict() for supply_request in supply_requests]

    def post(self):
        data = request.get_json()
        artwork_id = data.get('artwork_id')
        quantity = data.get('quantity')
        price = data.get('price')
        status = data.get('status')

        if not all([artwork_id, quantity, price, status]):
            return {'error': 'Missing data'}, 400

        supply_request = UserRequest(
            artwork_id=artwork_id,
            quantity=quantity,
            price=price,
            status=status
        )

        try:
            db.session.add(supply_request)
            db.session.commit()
            return supply_request.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class TransactionList(Resource):
    def get(self):
        transactions = Transaction.query.all()
        return [transaction.to_dict() for transaction in transactions]

class TransactionDetail(Resource):
    def get(self, transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return {'error': 'Transaction not found'}, 404
        return transaction.to_dict()

# Add the resources to the API
api.add_resource(Index, '/')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/checksession')
api.add_resource(UserList, '/users')
api.add_resource(ManageUser, '/users/<int:user_id>')
api.add_resource(UserDetails, '/user')
api.add_resource(Profile, '/profile')
api.add_resource(ArtworkList, '/Artworks')
api.add_resource(ArtworkDetail, '/Artwork/<int:artwork_id>')
api.add_resource(CreateArtwork, '/create_Artwork')
api.add_resource(PaymentList, '/payment')
api.add_resource(CategoryList, '/categories')
api.add_resource(ArtworksByCategory, '/categories/<int:category_id>/Artworks')
api.add_resource(ArtistList, '/Artists')
api.add_resource(ArtistArtworkList, '/ArtistArtwork')
api.add_resource(UserRequestList, '/UserRequest')
api.add_resource(TransactionList, '/transactions')
api.add_resource(TransactionDetail, '/transaction/<int:transaction_id>')

if __name__ == "__main__":
    app.run(port=5555)
