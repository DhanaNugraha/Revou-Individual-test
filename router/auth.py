from flask import Blueprint, request
from views.auth import user_login_view, user_register_view

auth_router = Blueprint("auth_router", __name__, url_prefix="/auth")


@auth_router.route("/register", methods=["POST"])
def user_register():
    return user_register_view(request.json)


@auth_router.route("/login", methods=["POST"])
def login():
    return user_login_view(request.json)