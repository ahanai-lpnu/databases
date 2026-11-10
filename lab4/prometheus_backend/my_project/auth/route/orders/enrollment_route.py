from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response, request
from my_project.auth.controller import enrollment_controller
from my_project.auth.domain.orders.models import CourseEnrollment

enrollment_bp = Blueprint("enrollments", __name__, url_prefix="/api/enrollments")


@enrollment_bp.get("")
def get_all_enrollments() -> Response:
    return make_response(jsonify(enrollment_controller.find_all()), HTTPStatus.OK)


@enrollment_bp.post("")
def create_enrollment() -> Response:
    content = request.get_json()
    enrollment = CourseEnrollment.create_from_dto(content)
    dto, status = enrollment_controller.create(enrollment)
    return make_response(jsonify(dto), status)


@enrollment_bp.delete("/<int:enrollment_id>")
def delete_enrollment(enrollment_id: int) -> Response:
    msg, status = enrollment_controller.delete(enrollment_id)
    return make_response(jsonify(msg), status)
