from functools import wraps
from flask import jsonify, request
from repo.user import user_by_id_repo

# used by middleware
# return user data except password
def claim_user_from_token(user_id_from_token):

    user = user_by_id_repo(user_id_from_token)

    filtered_user = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "address": user.address,
        "date_of_birth": user.date_of_birth,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "role": user.role
    }

    return filtered_user

# used by any function as wrapper
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = getattr(request, "user", None)

        if user is None:
            return jsonify({"message": "Unauthorized", "success": False, "location": "login_required auth"}), 401
        
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = getattr(request, "user", None)

        if user.get("role") != "admin":
            return jsonify({"message": "Admin access required", "success": False, "location": "admin_required auth"}), 403
        
        return f(*args, **kwargs)

    return decorated_function