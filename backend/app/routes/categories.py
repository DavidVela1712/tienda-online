from flask import Blueprint

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("/", methods=["GET"])
def list_categories():
    return {"message": "Categorias"}, 200