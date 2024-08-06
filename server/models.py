from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin #type: ignore
from marshmallow import Schema, fields

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    serialize_rules = ('-artworks.artist',)

    id =db.Column(db.Interger, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash =db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('artist', 'viewer', 'admin'), nullable=False, default='viewer')
    created_at = db.Column(db.Datetime, default=datetime,utcnow)

    artworks = db.relationship('Artwork', back_populates='artist')
    galleries = db.relationship('Gallery', back_populates='admin')
    orders = db.relationship('Order', back_populates='buyer')

class Artwork(db.Model, SerializerMixin):
    serialize_rules = ('-artist.artworks', '-gallery.artworks')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Integer, db.ForeignKey ('user.id'), nullable=False)
    image_url= db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    genre = db.Column(db.String(50), nullable=False)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable)

    artist = db.relationship('User', back_populates='artworks')
    gallery = db.relationship('Gallery', back_populates='artworks')
    orders = db.relationship('Order', back_populates='artwork')

class Gallery(db.Model, SerializerMixin):
    serialize_rules = ('artworks.gallery',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    admin = db.relationship('User', back_populates='galleries')
    artworks = db.relationship('Artwork', back_populates ='gallery')

