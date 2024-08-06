from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin #type: ignore
from marshmallow import Schema, fields

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    serialize_rules = ('-artworks.artist',)