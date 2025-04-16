from flask import jsonify
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from instance.database import db
from repo.user import register_user_repo, update_last_login_repo, user_by_email_repo
from schemas.auth import UserProfileResponse, UserRegisterRequest, UserLoginRequest

def user_register_view(user_request):
    # Validate request data
    try:
        user_data_validated = UserRegisterRequest.model_validate(user_request)

    except ValidationError as e:
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "view register user request validation"
        }), 400
    
    # Create user into database
    try:
        register_user_repo(user_data_validated)

    except Exception as e:  
        db.session.rollback()
        return jsonify(
            {"message": str(e), "success": False, "location": "view create user repo"},
        ), 500

    # return success
    return jsonify(
        {
            "data": {
                "message": f"{user_data_validated.email} registered successfully!"
            },
            "success": True,
        }
    ), 201


def user_login_view(user_request):
    # Validate request data
    try:
        user_data_validated = UserLoginRequest.model_validate(user_request)

    except ValidationError as e:
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "view login user request validation"
        }), 400
    
    # get user by email
    user = user_by_email_repo(user_data_validated.email)

    # check if user exist and if password is correct
    if not user or not user.verify_password(user_data_validated.password):
        return jsonify(
            {
                "message": "Invalid email or password",
                "success": False,
                "location": "view login user repo",
            }
        ), 401
    
    # create access token
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "username": user.username,
            "email": user.email,
            "is_vendor": user.is_vendor,
            "is_admin": user.is_admin,
        },
    )

    # update last login
    update_last_login_repo(user)

    return jsonify(
        {
            "success": True,
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_vendor": user.is_vendor,
                "is_admin": user.is_admin,
            },
        }
    ), 200


def get_user_view(user):
    # filter output and validate user data
    filtered_user_data = UserProfileResponse.model_validate(user)

    return jsonify({"success": True, "user": filtered_user_data.model_dump()}), 200
