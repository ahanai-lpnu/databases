from http import HTTPStatus
from typing import Any, Dict, List
from flask import abort
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service import category_service


class CategoryController(GeneralController):
    _service = category_service

    def get_categories_with_courses(self) -> List[Dict[str, Any]]:
        return self._service.get_categories_with_courses()

    def get_category_with_courses_by_id(self, category_id: int) -> Dict[str, Any]:
        res = self._service.get_category_with_courses_by_id(category_id)
        if res is None:
            abort(HTTPStatus.NOT_FOUND)
        return res
