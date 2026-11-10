from abc import ABC
from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO


class GeneralService(ABC):
    _dao: GeneralDAO

    def find_all(self) -> List[object]:
        return self._dao.find_all()

    def find_by_id(self, key: int) -> Optional[object]:
        return self._dao.find_by_id(key)

    def create(self, obj: object) -> object:
        return self._dao.create(obj)

    def update(self, key: int, obj: object) -> Optional[object]:
        return self._dao.update(key, obj)

    def delete(self, key: int) -> bool:
        return self._dao.delete(key)
