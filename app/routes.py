#routes.py
from app import app, db, ma, jwt
from models import User, Artwork

@app.route('/auth/signup', methods=['POST'])
def signup():Let us try and be flexible ,those available at 3 can meet then the major at 8:00
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = jwt.create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/artwork', methods=['GET'])
def get_artwork():
    artwork = Artwork.query.all()
    return jsonify([artwork.to_dict() for artwork in artwork]), 200
