from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response

err_handler_bp = Blueprint("errors", __name__)


@err_handler_bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def handle_404(error: int) -> Response:
    return make_response(jsonify({"error": "Resource not found"}), HTTPStatus.NOT_FOUND)
