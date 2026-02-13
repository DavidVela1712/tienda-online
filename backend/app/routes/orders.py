from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

order_service = OrderService()

@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Body vacío o no es JSON"}), 400

        items = data.get("items")
        total = data.get("total")

        if not items or not isinstance(items, list):
            return jsonify({"error": "No hay item o no es una lista"}), 400
        
        if total is None:
            return jsonify({"error": "Total inválido"}), 400
        
        order = order_service.create_order(data)

        return jsonify(order), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    
@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order = order_service.get_order_by_id(order_id)
        return jsonify(order), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@orders_bp.route("/", methods=["GET"])
def get_all_orders():
    try:
        status = request.args.get("status")
        orders = order_service.get_orders(status)
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@orders_bp.route("/<int:order_id>", methods=["PATCH"])
def change_order(order_id):
    try:
        new_order = request.get_json(silent=True)
        if new_order is None:
            return jsonify({"error": "Status vacío o no es JSON"}), 400
        if not isinstance(new_order.get("status"), str) or new_order.get("status") is None:
            return jsonify({"error": "Valor de status incorrecto"}), 400
        order = order_service.change_status(new_order.get("status"), order_id)
        return jsonify(order), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400