# app/blueprints/v1/auth.py - FIXED VERSION
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from pydantic import ValidationError
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import RegisterSchema, LoginSchema, ChangePasswordSchema
from app.models.user import User
from app.extensions import limiter

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    try:
        data = RegisterSchema(**request.json)
        
        user = AuthService.register_user(
            name=data.name,
            email=data.email,
            password=data.password
        )
        
        return jsonify({
            "message": "User registered successfully",
            "user": user.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Registration failed"}), 500

@bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        data = LoginSchema(**request.json)
        
        user = AuthService.authenticate(data.email, data.password)
        access_token, refresh_token = AuthService.create_tokens(user)
        
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500

@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id_str = get_jwt_identity()  # This will be a string
        access_token = AuthService.refresh_access_token(user_id_str)
        
        return jsonify({
            "access_token": access_token
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Token refresh failed"}), 500

@bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    try:
        user_id_str = get_jwt_identity()  # This will be a string
        claims = get_jwt()
        
        # FIXED: Convert string ID back to int for database query
        user_id = int(user_id_str)
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({"user": user.to_dict()}), 200
        
    except ValueError:
        return jsonify({"error": "Invalid user ID"}), 400
    except Exception as e:
        return jsonify({"error": "Failed to get profile"}), 500

@bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    try:
        data = ChangePasswordSchema(**request.json)
        user_id_str = get_jwt_identity()  # This will be a string
        
        AuthService.change_password(
            user_id_str=user_id_str,
            current_password=data.current_password,
            new_password=data.new_password
        )
        
        return jsonify({"message": "Password changed successfully"}), 200
        
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Password change failed"}), 500