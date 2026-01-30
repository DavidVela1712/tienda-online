from datetime import datetime
import uuid

class OrderService:
    def __init__(self):
        self.orders = []

    
    def create_order(self, data):
        items = data.get("items", [])
        if items == []:
            order = {
            "id": str(uuid.uuid4()),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "items": data.get("items", []),
            }
            self.orders.append(order)
            # prueba
            return order
        else:
            raise ValueError("La edad no puede ser negativa.")