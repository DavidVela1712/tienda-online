from app.extensions import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    descripcion = db.Column(db.String(100))
    imagen = db.Column(db.String(20))
    categoria_id = db.Column(db.Integer)
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)
    activo = db.Column(db.String(20), default="activo")