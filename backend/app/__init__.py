from flask import Flask
from app.routes.health import health_bp
from app.routes.products import products_bp
from app.routes.orders import orders_bp
from app.routes.categories import categories_bp

def crate_app():
    app = Flask(__name__)

    app.register_blueprint(health_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(categories_bp)
    
    return app