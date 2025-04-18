from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from views.product import create_product_view, get_product_detail_view, list_products_view


products_router = Blueprint("products_router", __name__, url_prefix="/products")


@products_router.route("", methods=["POST"])
@jwt_required()
def create_product():
    return create_product_view(current_user, request.json)

# public path
@products_router.route("", methods=["GET"])
def list_products():
    return list_products_view(request.args)

@products_router.route("/<int:product_id>", methods=["GET"])
def get_product_detail(product_id):
    return get_product_detail_view(product_id)