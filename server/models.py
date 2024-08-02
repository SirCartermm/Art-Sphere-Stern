# app/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    serialize_rules = ('-artworks.artist',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='viewer')  # Roles: admin, artist, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    artworks = db.relationship('Artwork', back_populates='artist')
 
class Admin(db.Model, SerializerMixin):
    serialize_rules = ('-artworks.admin',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='admin')  # Roles: admin, artist, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    artworks = db.relationship('Artwork', back_populates='admin')

class Artists(db.Model, SerializerMixin):
    serialize_rules = ('-artworks.artists',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artworks = db.relationship('Artwork', back_populates='artists')
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable=True)
    orders = db.relationship('Order', back_populates='artists')
    orders_history = db.relationship('Order', back_populates='artists_history')
    orders_cancelled = db.relationship('Order', back_populates='artists_cancelled')
    orders_completed = db.relationship('Order', back_populates='artists_completed')
    orders_refunded = db.relationship('Order', back_populates='artists_refunded')
    orders_disputed = db.relationship('Order', back_populates='artists_disputed')
    orders_returned = db.relationship('Order', back_populates='artists_returned')

   
artworks = db.relationship('Artwork', back_populates='artists_artworks')


class Artwork(db.Model, SerializerMixin):
    serialize_rules = ('-artist.artworks', '-gallery.artworks')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable=True)

    artist = db.relationship('User', back_populates='artworks')
    gallery = db.relationship('Gallery', back_populates='artworks')

class Gallery(db.Model, SerializerMixin):
    serialize_rules = ('-artworks.gallery',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    artworks = db.relationship('Artwork', back_populates='gallery')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # States: Pending, Confirmed, Shipped, Delivered, Completed
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    digital_certificate = db.Column(db.String(255), nullable=True)