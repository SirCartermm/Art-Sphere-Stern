#routes.py
from app import app, db, ma, jwt
from models import User, Artwork

@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}, 201)
