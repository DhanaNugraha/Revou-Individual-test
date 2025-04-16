from flask import Blueprint, request
from views.auth import user_register_view

auth_router = Blueprint("auth_router", __name__, url_prefix="/auth")


@auth_router.route("/register", methods=["POST"])
def user_register():
    return user_register_view(request.json)
