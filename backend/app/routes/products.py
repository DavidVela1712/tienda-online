from flask import Blueprint
from app.services.product_service import ProductService
products_bp = Blueprint("products", __name__, url_prefix="/products")

product_service = ProductService()

@products_bp.route("/", methods=["GET"])
def list_products():
    products = product_service.list_products()
    return {"products": products}, 200