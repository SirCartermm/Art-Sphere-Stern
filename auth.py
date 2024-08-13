from flask import jsonify, request
from app import app, jwt , db
from models import User
from modelsUser,  imports User # type: ignore

@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user) # type: ignore
    db.session.commit() # type: ignore
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = jwt.create_access_token(identify=user.id)
        return jsonify ({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/auth/logout', methods=['POST'])
@jwt_required
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

# Artwork Endpoints 
