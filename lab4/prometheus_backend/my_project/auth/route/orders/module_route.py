from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response, request
from my_project.auth.controller import module_controller
from my_project.auth.domain.orders.models import Module

module_bp = Blueprint("modules", __name__, url_prefix="/api/modules")


@module_bp.get("")
def get_all_modules() -> Response:
    return make_response(jsonify(module_controller.find_all()), HTTPStatus.OK)


@module_bp.get("/<int:module_id>")
def get_module(module_id: int) -> Response:
    return make_response(jsonify(module_controller.find_by_id(module_id)), HTTPStatus.OK)


@module_bp.post("")
def create_module() -> Response:
    content = request.get_json()
    module = Module.create_from_dto(content)
    dto, status = module_controller.create(module)
    return make_response(jsonify(dto), status)


@module_bp.put("/<int:module_id>")
def update_module(module_id: int) -> Response:
    content = request.get_json()
    module = Module.create_from_dto(content)
    return make_response(jsonify(module_controller.update(module_id, module)), HTTPStatus.OK)


@module_bp.delete("/<int:module_id>")
def delete_module(module_id: int) -> Response:
    msg, status = module_controller.delete(module_id)
    return make_response(jsonify(msg), status)
