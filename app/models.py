from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy import Enum
import enum

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

# Enum for user roles
class Role(enum.Enum):
    artist = 'artist'
    viewer = 'viewer'
    admin = 'admin'

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(Enum(Role), nullable=False)

    # Relationship to artworks
    artworks = db.relationship('Artwork', backref='artist', lazy=True)

    # Relationship to galleries
    galleries = db.relationship('Gallery', backref='admin', lazy=True)

# Artwork model
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Example: Decimal(10, 2) for currency
    genre = db.Column(db.String(100), nullable=True)

    # Relationship to artist (User)
    artist = db.relationship('User', backref=db.backref('artworks', lazy=True))

    # Relationship to galleries
    galleries = db.relationship('Gallery', secondary='artwork_gallery', backref='artworks')

# Gallery model
class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to admin (User)
    admin = db.relationship('User', backref=db.backref('galleries', lazy=True))

    # Relationship to artworks
    artworks = db.relationship('Artwork', secondary='artwork_gallery', backref='galleries')

# Association table for many-to-many relationship between Artwork and Gallery
class ArtworkGallery(db.Model):
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), primary_key=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), primary_key=True)

    # Relationships
    artwork = db.relationship('Artwork', backref=db.backref('artwork_galleries'))
    gallery = db.relationship('Gallery', backref=db.backref('artwork_galleries'))
