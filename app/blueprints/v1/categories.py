# app/blueprints/v1/categories.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.services.category_service import CategoryService
from app.schemas.category_schemas import CategoryCreateSchema, CategoryUpdateSchema
from app.utils.decorators import role_required

bp = Blueprint("categories", __name__)

@bp.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    try:
        categories = CategoryService.get_all_categories()
        
        return jsonify({
            "categories": [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch categories"}), 500

@bp.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    try:
        category = CategoryService.get_category_by_id(category_id)
        
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        return jsonify({"category": category.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch category"}), 500

@bp.route("/", methods=["POST"])
@role_required("Admin")
def create_category():
    try:
        # Validate input data
        data = CategoryCreateSchema(**request.json)
        
        # Create category
        category = CategoryService.create_category(name=data.name)
        
        return jsonify({
            "message": "Category created successfully",
            "category": category.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Category creation failed"}), 500

@bp.route("/<int:category_id>", methods=["PUT"])
@role_required("Admin")
def update_category(category_id):
    try:
        # Validate input data
        data = CategoryUpdateSchema(**request.json)
        
        # Update category
        category = CategoryService.update_category(
            category_id=category_id,
            name=data.name
        )
        
        return jsonify({
            "message": "Category updated successfully",
            "category": category.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Category update failed"}), 500

@bp.route("/<int:category_id>", methods=["DELETE"])
@role_required("Admin")
def delete_category(category_id):
    try:
        CategoryService.delete_category(category_id)
        
        return jsonify({"message": "Category deleted successfully"}), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Category deletion failed"}), 500


# # app/blueprints/v1/health.py
# from flask import Blueprint, jsonify

# bp = Blueprint("health", __name__)

# @bp.route("/", methods=["GET"])
# def health_check():
#     return jsonify({
#         "status": "healthy",
#         "message": "Product Management API is running",
#         "version": "1.0.0"
#     }), 200