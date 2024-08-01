from app import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.string(128))
    role = db.column(db.Enum('artist', 'viewer', 'admin'))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password) # type: ignore

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password) # type: ignore
    
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.column(db.Integer, db.Foreignkey('user.id'))
    title = db.Column(db.string(128), nullable=False)
    description = db.column(db.Text)
    image_url = db.Column(db.String(128))
    price = db.Column(db.DECIMAL(10, 2))
    genre = db.Column(db.String(64))

 
                      
                