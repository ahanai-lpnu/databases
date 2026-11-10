from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response, request
from my_project.auth.controller import category_controller
from my_project.auth.domain.orders.models import Category

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@category_bp.get("")
def get_all_categories() -> Response:
    return make_response(jsonify(category_controller.find_all()), HTTPStatus.OK)


@category_bp.get("/<int:category_id>")
def get_category(category_id: int) -> Response:
    return make_response(jsonify(category_controller.find_by_id(category_id)), HTTPStatus.OK)


@category_bp.post("")
def create_category() -> Response:
    content = request.get_json()
    category = Category.create_from_dto(content)
    dto, status = category_controller.create(category)
    return make_response(jsonify(dto), status)


@category_bp.put("/<int:category_id>")
def update_category(category_id: int) -> Response:
    content = request.get_json()
    category = Category.create_from_dto(content)
    return make_response(jsonify(category_controller.update(category_id, category)), HTTPStatus.OK)


@category_bp.delete("/<int:category_id>")
def delete_category(category_id: int) -> Response:
    msg, status = category_controller.delete(category_id)
    return make_response(jsonify(msg), status)


@category_bp.get("/with-courses")
def get_categories_with_courses() -> Response:
    return make_response(jsonify(category_controller.get_categories_with_courses()), HTTPStatus.OK)


@category_bp.get("/<int:category_id>/courses")
def get_category_courses(category_id: int) -> Response:
    return make_response(jsonify(category_controller.get_category_with_courses_by_id(category_id)), HTTPStatus.OK)
