from app import app, db
from models import User, Artwork, Category, Payment, ArtistArtwork, UserRequest, Artist, Transaction
from werkzeug.security import generate_password_hash
from datetime import datetime

# Initialize the app and the database
app.app_context().push()

def create_categories():
    categories = ['Painting', 'Sculpture', 'Photography', 'Digital Art']
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()

def create_artists():
    artists = ['Vincent van Gogh', 'Pablo Picasso', 'Claude Monet', 'Frida Kahlo']
    for name in artists:
        artist = Artist(name=name)
        db.session.add(artist)
    db.session.commit()

def create_users():
    users = [
        {'name': 'Admin User', 'email': 'admin@example.com', 'password': 'password', 'role': 'Admin'},
        {'name': 'Regular User', 'email': 'user@example.com', 'password': 'password', 'role': 'User'}
    ]
    for user in users:
        new_user = User(
            name=user['name'],
            email=user['email'],
            password=generate_password_hash(user['password']),
            role=user['role']
        )
        db.session.add(new_user)
    db.session.commit()

def create_artworks():
    artworks = [
        {'name': 'Starry Night', 'category_id': 1, 'bp': 1000.00, 'sp': 1200.00},
        {'name': 'Guernica', 'category_id': 2, 'bp': 1500.00, 'sp': 1800.00},
        {'name': 'Water Lilies', 'category_id': 3, 'bp': 800.00, 'sp': 1000.00},
        {'name': 'The Two Fridas', 'category_id': 4, 'bp': 2000.00, 'sp': 2500.00}
    ]
    for artwork in artworks:
        new_artwork = Artwork(
            name=artwork['name'],
            category_id=artwork['category_id'],
            bp=artwork['bp'],
            sp=artwork['sp']
        )
        db.session.add(new_artwork)
    db.session.commit()

def create_payments():
    payments = [
        {'inventory_id': 1, 'amount': 1000.00, 'payment_date': datetime.utcnow()},
        {'inventory_id': 2, 'amount': 1500.00, 'payment_date': datetime.utcnow()}
    ]
    for payment in payments:
        new_payment = Payment(
            inventory_id=payment['inventory_id'],
            amount=payment['amount'],
            payment_date=payment['payment_date']
        )
        db.session.add(new_payment)
    db.session.commit()

def create_artist_artworks():
    artist_artworks = [
        {'artwork_id': 1, 'artist_id': 1, 'price': 1200.00},
        {'artwork_id': 2, 'artist_id': 2, 'price': 1800.00}
    ]
    for artist_artwork in artist_artworks:
        new_artist_artwork = ArtistArtwork(
            artwork_id=artist_artwork['artwork_id'],
            artist_id=artist_artwork['artist_id'],
            price=artist_artwork['price']
        )
        db.session.add(new_artist_artwork)
    db.session.commit()

def create_user_requests():
    user_requests = [
        {'artwork_id': 1, 'quantity': 2, 'price': 1200.00, 'status': 'Pending'},
        {'artwork_id': 3, 'quantity': 1, 'price': 1000.00, 'status': 'Completed'}
    ]
    for user_request in user_requests:
        new_user_request = UserRequest(
            artwork_id=user_request['artwork_id'],
            quantity=user_request['quantity'],
            price=user_request['price'],
            status=user_request['status']
        )
        db.session.add(new_user_request)
    db.session.commit()

def create_transactions():
    transactions = [
        {'user_id': 1, 'artwork_id': 1, 'amount': 1200.00, 'transaction_date': datetime.utcnow()},
        {'user_id': 2, 'artwork_id': 3, 'amount': 1000.00, 'transaction_date': datetime.utcnow()}
    ]
    for transaction in transactions:
        new_transaction = Transaction(
            user_id=transaction['user_id'],
            artwork_id=transaction['artwork_id'],
            amount=transaction['amount'],
            transaction_date=transaction['transaction_date']
        )
        db.session.add(new_transaction)
    db.session.commit()

def seed_database():
    create_categories()
    create_artists()
    create_users()
    create_artworks()
    create_payments()
    create_artist_artworks()
    create_user_requests()
    create_transactions()
    print("Database seeded successfully!")

if __name__ == '_main_':
    seed_database()
