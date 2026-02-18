from app.extensions import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    image = db.Column(db.String(20))
    categoria_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    active = db.Column(db.String(20), default="activo")