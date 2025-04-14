from flask import request
from auth.auth import claim_user_from_token
from flask_jwt_extended import get_jwt_identity, jwt_required


def auth_middleware(app):
    @app.before_request
    @jwt_required(optional=True)
    def before_request():
        user_id_from_token = get_jwt_identity()

        if user_id_from_token:
            request.user = claim_user_from_token(user_id_from_token)

