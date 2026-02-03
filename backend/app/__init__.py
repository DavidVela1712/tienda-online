from flask import Flask
from app.routes.health import health_bp
from app.routes.products import products_bp
from app.routes.orders import orders_bp
from app.routes.categories import categories_bp
from app.extensions import db

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(categories_bp)
    
    return app