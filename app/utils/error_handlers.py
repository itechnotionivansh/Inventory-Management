# app/utils/error_handlers.py
from flask import jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from flask_jwt_extended.exceptions import JWTExtendedException

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            "error": "Validation failed",
            "details": e.errors()
        }), 400

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "error": e.description,
            "code": e.code
        }), e.code

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_exceptions(e):
        return jsonify({"error": str(e)}), 401

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({"error": "Internal server error"}), 500