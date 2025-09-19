# app/blueprints/v1/products.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from pydantic import ValidationError
from app.services.product_service import ProductService
from app.schemas.product_schemas import ProductCreateSchema, ProductUpdateSchema
from app.utils.decorators import role_required

bp = Blueprint("products", __name__)

@bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        
        if category:
            products = ProductService.get_products_by_category(category)
        elif search:
            products = ProductService.search_products(search)
        else:
            products = ProductService.get_all_products()
        
        return jsonify({
            "products": [product.to_dict() for product in products]
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch products"}), 500

@bp.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    try:
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        return jsonify({"product": product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch product"}), 500

@bp.route("/", methods=["POST"])
@role_required("Admin")
def create_product():
    try:
        # Validate input data
        data = ProductCreateSchema(**request.json)
        user_id = get_jwt_identity()
        
        # Create product
        product = ProductService.create_product(
            name=data.name,
            price=data.price,
            colors=data.colors,
            tags=data.tags,
            category_name=data.category_name,
            uploader_id=user_id
        )
        
        return jsonify({
            "message": "Product created successfully",
            "product": product.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Product creation failed"}), 500

@bp.route("/<int:product_id>", methods=["PUT"])
@role_required("Admin")
def update_product(product_id):
    try:
        # Validate input data
        data = ProductUpdateSchema(**request.json)
        
        # Update product
        product = ProductService.update_product(
            product_id=product_id,
            name=data.name,
            price=data.price,
            colors=data.colors,
            tags=data.tags,
            category_name=data.category_name
        )
        
        return jsonify({
            "message": "Product updated successfully",
            "product": product.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Product update failed"}), 500

@bp.route("/<int:product_id>", methods=["DELETE"])
@role_required("Admin")
def delete_product(product_id):
    try:
        ProductService.delete_product(product_id)
        
        return jsonify({"message": "Product deleted successfully"}), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Product deletion failed"}), 500