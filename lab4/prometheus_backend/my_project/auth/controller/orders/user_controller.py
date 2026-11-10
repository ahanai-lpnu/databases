from http import HTTPStatus
from typing import Any, Dict, List
from flask import abort
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service import user_service


class UserController(GeneralController):
    _service = user_service

    def get_users_with_enrolled_courses(self) -> List[Dict[str, Any]]:
        return self._service.get_users_with_enrolled_courses()

    def get_user_courses_by_id(self, user_id: int) -> Dict[str, Any]:
        res = self._service.get_user_courses_by_id(user_id)
        if res is None:
            abort(HTTPStatus.NOT_FOUND)
        return res
