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