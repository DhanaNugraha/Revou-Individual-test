from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.user import register_user_repo
from schemas.auth import UserRegisterRequest

def user_register_view(user_request):
    # Validate request data
    try:
        user_data_validated = UserRegisterRequest.model_validate(user_request)

    except ValidationError as e:
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "request validation"
        }), 400
    
    try:
        register_user_repo(user_data_validated)

    except Exception as e:  
        db.session.rollback()
        return jsonify(
            {"message": str(e), "success": False, "location": "create user repo"},
        ), 500

    return jsonify(
        {
            "data": {
                "message": f"{user_data_validated.email} registered successfully!"
            },
            "success": True,
        } 
    )

