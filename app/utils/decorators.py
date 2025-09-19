# app/utils/decorators.py - FIXED VERSION
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(*required_roles):
    """
    Decorator to restrict access to users with specific roles.
    Usage: @role_required("Admin"), or @role_required("Admin", "Manager")
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')

            if not user_role or user_role not in required_roles:
                return jsonify({
                    "error": "Forbidden - insufficient permissions",
                    "required_roles": list(required_roles),
                    "user_role": user_role
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper