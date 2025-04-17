from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from views.product import create_product_view


products_router = Blueprint("products_router", __name__, url_prefix="/products")


@products_router.route("", methods=["POST"])
@jwt_required()
def create_product():
    return create_product_view(current_user, request.json)