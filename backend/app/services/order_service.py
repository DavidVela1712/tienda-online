from datetime import datetime
import uuid
from app.extensions import db

from app.model.order import Order, OrderItem


class OrderService:
    def __init__(self):
        self.orders = []

    def create_order(self, data):
        items = data.get("items")
        calculated_total = 0
        if isinstance(items, list) and items != []:
            for item in items:
                if (
                    item.get("product_id") is None
                    or item.get("quantity") is None
                    or item.get("price") is None
                ):
                    raise ValueError("Valores no esperados")
                calculated_total += item.get("quantity") * item.get("price")
            if data.get("total") != calculated_total:
                raise ValueError("Totales distintos")

            order = Order(
                user_id=0,
                status="pending",
                total_amount=calculated_total,
            )
            db.session.add(order)
            db.session.flush()
            order_items_list = []
            for item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.get("product_id"),
                    quantity=item.get("quantity"),
                    unit_price=item.get("unit_price"),
                )
                db.session.add(order_item)
                order_items_list.append(order_item)
            db.session.commit()

            order_dict = {
                "id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "created_at": order.created_at,
                "total_amount": order.total_amount,
                "items": [],
            }

            for oi in order_items_list:
                order_dict["items"].append(
                    {
                        "product_id": oi.product_id,
                        "quantity": oi.quantity,
                        "unit_price": oi.unit_price,
                    }
                )

            return order_dict
        
    def get_order_by_id(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order no encontrado")
        else:
            order_dict = {
                "id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "total_amount": order.total_amount,
                "items": [],
            }
            for item in order.items:
                order_dict["items"].append(
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                    }
                )
            return order_dict
