from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response, request
from my_project.auth.controller import user_controller
from my_project.auth.domain.orders.models import User

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.get("")
def get_all_users() -> Response:
    return make_response(jsonify(user_controller.find_all()), HTTPStatus.OK)


@user_bp.get("/<int:user_id>")
def get_user(user_id: int) -> Response:
    return make_response(jsonify(user_controller.find_by_id(user_id)), HTTPStatus.OK)


@user_bp.post("")
def create_user() -> Response:
    content = request.get_json()
    user = User.create_from_dto(content)
    dto, status = user_controller.create(user)
    return make_response(jsonify(dto), status)


@user_bp.put("/<int:user_id>")
def update_user(user_id: int) -> Response:
    content = request.get_json()
    user = User.create_from_dto(content)
    return make_response(jsonify(user_controller.update(user_id, user)), HTTPStatus.OK)


@user_bp.delete("/<int:user_id>")
def delete_user(user_id: int) -> Response:
    msg, status = user_controller.delete(user_id)
    return make_response(jsonify(msg), status)


@user_bp.get("/with-courses")
def get_users_with_courses() -> Response:
    return make_response(jsonify(user_controller.get_users_with_enrolled_courses()), HTTPStatus.OK)


@user_bp.get("/<int:user_id>/courses")
def get_user_courses(user_id: int) -> Response:
    return make_response(jsonify(user_controller.get_user_courses_by_id(user_id)), HTTPStatus.OK)
