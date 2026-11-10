from http import HTTPStatus
from typing import Any, Dict, List
from flask import abort
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service import course_service


class CourseController(GeneralController):
    _service = course_service

    def get_courses_with_modules(self) -> List[Dict[str, Any]]:
        return self._service.get_courses_with_modules()

    def get_courses_with_enrolled_students(self) -> List[Dict[str, Any]]:
        return self._service.get_courses_with_enrolled_students()

    def get_course_students_by_id(self, course_id: int) -> Dict[str, Any]:
        res = self._service.get_course_students_by_id(course_id)
        if res is None:
            abort(HTTPStatus.NOT_FOUND)
        return res
