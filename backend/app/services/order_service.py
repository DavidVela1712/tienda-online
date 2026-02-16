from datetime import datetime
import uuid
from app.extensions import db

from app.model.order import Order, OrderItem
from app.model.product import Product


status_list = ["pending", "paid", "shipped", "cancelled", "closed"]


class OrderService:

    def create_order(self, data):
        items = data.get("items")
        calculated_total = 0
        if isinstance(items, list) and items != []:
            products_to_update = []
            for item in items:
                if (
                    item.get("product_id") is None
                    or item.get("quantity") is None
                ):
                    raise ValueError("Valores no esperados")
                
                if item.get("quantity") <= 0:
                    raise ValueError("Cantidad inválida")
                
                product = Product.query.get(item.get("product_id"))
                if not product:
                    raise ValueError("Producto no encontrado")

                if product.stock < item.get("quantity"):
                    raise ValueError("Stock insuficiente")
                products_to_update.append((product, item.get("quantity")))
                calculated_total += item.get("quantity") * product.price
            
            order = Order(
                user_id=data.get("user_id"),
                status="pending",
                total_amount=calculated_total,
            )
            db.session.add(order)
            db.session.flush()

            order_items_list = []
            for product, quantity in products_to_update:
                product.stock -= quantity
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
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

    def get_orders(self, status=None):
        if status and status not in status_list:
            raise ValueError("Status incorrecto")
        if status:
            orders = Order.query.filter_by(status=status).all()
        else:
            orders = Order.query.all()
        orders_list = []
        for order in orders:
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
            orders_list.append(order_dict)
        return orders_list

    def change_status(self, new_status, order_id):
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Pedido no encontrado")
        else:
            if new_status not in status_list:
                raise ValueError("Status incorrecto")
            elif order.status in ["pending", "paid"] and new_status == "cancelled":
                for item in order.items:
                    product = Product.query.get(item.product_id)
                    product.stock += item.quantity
                order.status = new_status
            elif order.status == "pending" and new_status == "paid":
                order.status = new_status
            elif order.status == "paid" and new_status == "shipped":
                order.status = new_status
            elif order.status == "shipped" and new_status == "closed":
                order.status = new_status
            else:
                raise ValueError("No se puede modificar ese Status")
            db.session.commit()
            return order
