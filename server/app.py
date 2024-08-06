from flask import Blueprint, jsonify, request
from flask_jwt extended import jwt_required, get_jwt_idntity
from datetime import Gallery, Order
from.models import Gallery, Order
from .schemas import OrderSchema

gallery_routes =Blueprint('gallery_routes', __name__)
order_routes = Blueprint('order_routes', __name__)

@gallery_routes.route('/gallery', methods=['GET'])
def get_galleries():
    galleries = Gallery.query.all()
    return jsonify([{'id': gallery.id,'name': gallery.name, 'admin_id': gallery.admin_id}
                  for gallery in galleries])

@gallery_routes.route('/gallery/<int:gallery_id>', methods=['GET'])
def get_gallery(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    
    
