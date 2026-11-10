from typing import Any, Dict, List, Optional
from my_project.auth.dao import course_dao
from my_project.auth.service.general_service import GeneralService


class CourseService(GeneralService):
    _dao = course_dao

    def get_courses_with_modules(self) -> List[Dict[str, Any]]:
        return [
            {**course.put_into_dto(), "modules": [m.put_into_dto() for m in course.modules]}
            for course in self._dao.find_all()
        ]

    def get_courses_with_enrolled_students(self) -> List[Dict[str, Any]]:
        result = []
        for course in self._dao.find_all():
            dto = course.put_into_dto()
            dto["enrolled_students"] = [
                {
                    "enrollment_id": enr.id,
                    "status": enr.status,
                    "student": enr.student.put_into_dto(),
                }
                for enr in course.enrollments
            ]
            result.append(dto)
        return result

    def get_course_students_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        course = self._dao.find_by_id(course_id)
        if not course:
            return None
        dto = course.put_into_dto()
        dto["enrolled_students"] = [
            {"enrollment_id": enr.id, "status": enr.status, "student": enr.student.put_into_dto()}
            for enr in course.enrollments
        ]
        return dto
