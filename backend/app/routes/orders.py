from flask import Blueprint, request
from app.services.order_service import OrderService

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

order_service = OrderService()

@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        data = request.get_json(silent=True)
        if isinstance(data.get("items", []), list):
            order = order_service.create_order(data)
            return order, 201
        else:
            return "Error al crear el pedido", 400
    except:
        return "Error al crear el pedido", 400