from flask import Blueprint
from flask_restful import Resource,Api,reqparse


from flask import Blueprint, request, jsonify
from app.models import Order

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/', methods=['POST'])
def place_order():
    data = request.get_json()
    user_id = data['user_id']
    artwork_id = data['artwork_id']
    quantity = data['quantity']

    new_order = Order(user_id=user_id, artwork_id=artwork_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'}), 201

@bp.route('/', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return jsonify([{'id': o.id, 'user_id': o.user_id, 'artwork_id': o.artwork_id, 'quantity': o.quantity} for o in orders]), 200

order_bp=Blueprint('order',__name__,url_prefix='/orders')