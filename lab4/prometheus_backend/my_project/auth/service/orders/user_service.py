from typing import Any, Dict, List, Optional
from my_project.auth.dao import user_dao
from my_project.auth.service.general_service import GeneralService


class UserService(GeneralService):
    _dao = user_dao

    def get_users_with_enrolled_courses(self) -> List[Dict[str, Any]]:
        result = []
        for user in self._dao.find_all():
            dto = user.put_into_dto()
            dto["enrolled_courses"] = [
                {"enrollment_id": enr.id, "status": enr.status, "course": enr.course.put_into_dto()}
                for enr in user.enrollments
            ]
            result.append(dto)
        return result

    def get_user_courses_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        user = self._dao.find_by_id(user_id)
        if not user:
            return None
        dto = user.put_into_dto()
        dto["enrolled_courses"] = [
            {"enrollment_id": enr.id, "status": enr.status, "course": enr.course.put_into_dto()}
            for enr in user.enrollments
        ]
        return dto
