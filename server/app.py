from flask import Blueprint, jsonify, request  
from flask_jwt_extended import jwt_required, get_jwt_identity   # type: ignore
from datetime import datetime  
from .models import Gallery, Order  
from .schemas import OrderSchema   # type: ignore
from payment import create_payment_intent

gallery_routes = Blueprint('gallery_routes', __name__)  
order_routes = Blueprint('order_routes', __name__)  

@gallery_routes.route('/gallery', methods=['GET'])  
def get_galleries():  
    galleries = Gallery.query.all()  
    return jsonify([{'id': gallery.id, 'name': gallery.name, 'admin_id': gallery.admin_id}  
                   for gallery in galleries])  

@gallery_routes.route('/gallery/<int:gallery_id>', methods=['GET'])  
def get_gallery(gallery_id):  
    gallery = Gallery.query.get(gallery_id)  
    if gallery:  
        return jsonify({'id': gallery.id, 'name': gallery.name, 'admin_id': gallery.admin_id})  
    return jsonify({'message': 'Gallery not found'}), 404  

@gallery_routes.route('/gallery', methods=['POST'])  
@jwt_required  
def create_gallery():  
    data = request.get_json()  
    gallery = Gallery(name=data['name'], admin_id=get_jwt_identity())  
    db.session.add(gallery)   # type: ignore
    db.session.commit()   # type: ignore
    return jsonify({'message': 'Gallery created successfully'}), 201  

@gallery_routes.route('/gallery/<int:gallery_id>', methods=['PUT'])  
@jwt_required  
def update_gallery(gallery_id):  
    gallery = Gallery.query.get(gallery_id)  
    if gallery:  
        data = request.get_json()  
        gallery.name = data['name']  
        db.session.commit()   # type: ignore
        return jsonify({'message': 'Gallery updated successfully'})  
    return jsonify({'message': 'Gallery not found'}), 404  

@gallery_routes.route('/gallery/<int:gallery_id>', methods=['DELETE'])  
@jwt_required  
def delete_gallery(gallery_id):  
    gallery = Gallery.query.get(gallery_id)  
    if gallery:  
        db.session.delete(gallery)   # type: ignore
        db.session.commit()   # type: ignore
        return jsonify({'message': 'Gallery deleted successfully'})  
    return jsonify({'message': 'Gallery not found'}), 404  

@order_routes.route('/order', methods=['POST'])  
@jwt_required  
def create_order():  
    data = request.get_json()  
    order = Order(user_id=get_jwt_identity(), artwork_id=data['artwork_id'], purchase_date=datetime.utcnow())  
    db.session.add(order)   # type: ignore
    db.session.commit()   # type: ignore
    return jsonify({'message': 'Order created successfully'}), 201  

@order_routes.route('/order/<int:order_id>', methods=['GET'])  
@jwt_required  
def get_order(order_id):  
    order = Order.query.get(order_id)  
    if order:  
        schema = OrderSchema()  
        return jsonify(schema.dump(order))  
    return jsonify({'message': 'Order not found'}), 404  


@app.route('/payment', methods=['POST'])
@jwt_required
def process_payment():
    data = request.get_json()
    amount = data['amount']
    currency = data['currency']
    intent = create_payment_intent(amount, currency)
    return jsonify(intent), 200
