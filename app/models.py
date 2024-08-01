# models.py
from app import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.string(128))
    role = db.column(db.Enum('artist', 'viewer', 'admin'))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    