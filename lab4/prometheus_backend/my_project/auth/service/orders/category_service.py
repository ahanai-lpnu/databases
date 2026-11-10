from typing import Any, Dict, List, Optional
from my_project.auth.dao import category_dao
from my_project.auth.service.general_service import GeneralService


class CategoryService(GeneralService):
    _dao = category_dao

    def get_categories_with_courses(self) -> List[Dict[str, Any]]:
        return [
            {**cat.put_into_dto(), "courses": [c.put_into_dto() for c in cat.courses]}
            for cat in self._dao.find_all()
        ]

    def get_category_with_courses_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        cat = self._dao.find_by_id(category_id)
        if not cat:
            return None
        return {**cat.put_into_dto(), "courses": [c.put_into_dto() for c in cat.courses]}
