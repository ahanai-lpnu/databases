from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response, request
from my_project.auth.controller import course_controller
from my_project.auth.domain.orders.models import Course

course_bp = Blueprint("courses", __name__, url_prefix="/api/courses")


@course_bp.get("")
def get_all_courses() -> Response:
    return make_response(jsonify(course_controller.find_all()), HTTPStatus.OK)


@course_bp.get("/<int:course_id>")
def get_course(course_id: int) -> Response:
    return make_response(jsonify(course_controller.find_by_id(course_id)), HTTPStatus.OK)


@course_bp.post("")
def create_course() -> Response:
    content = request.get_json()
    course = Course.create_from_dto(content)
    dto, status = course_controller.create(course)
    return make_response(jsonify(dto), status)


@course_bp.put("/<int:course_id>")
def update_course(course_id: int) -> Response:
    content = request.get_json()
    course = Course.create_from_dto(content)
    return make_response(jsonify(course_controller.update(course_id, course)), HTTPStatus.OK)


@course_bp.delete("/<int:course_id>")
def delete_course(course_id: int) -> Response:
    msg, status = course_controller.delete(course_id)
    return make_response(jsonify(msg), status)


@course_bp.get("/with-modules")
def get_courses_with_modules() -> Response:
    return make_response(jsonify(course_controller.get_courses_with_modules()), HTTPStatus.OK)


@course_bp.get("/with-students")
def get_courses_with_students() -> Response:
    return make_response(jsonify(course_controller.get_courses_with_enrolled_students()), HTTPStatus.OK)


@course_bp.get("/<int:course_id>/students")
def get_course_students(course_id: int) -> Response:
    return make_response(jsonify(course_controller.get_course_students_by_id(course_id)), HTTPStatus.OK)
