from abc import ABC
from http import HTTPStatus
from typing import Any, Dict, List, Tuple
from flask import abort
from my_project.auth.service.general_service import GeneralService


class GeneralController(ABC):
    _service: GeneralService

    def find_all(self) -> List[Dict[str, Any]]:
        return [x.put_into_dto() for x in self._service.find_all()]

    def find_by_id(self, key: int) -> Dict[str, Any]:
        obj = self._service.find_by_id(key)
        if obj is None:
            abort(HTTPStatus.NOT_FOUND)
        return obj.put_into_dto()

    def create(self, obj: object) -> Tuple[Dict[str, Any], int]:
        created = self._service.create(obj)
        return created.put_into_dto(), HTTPStatus.CREATED

    def update(self, key: int, obj: object) -> Dict[str, Any]:
        updated = self._service.update(key, obj)
        if updated is None:
            abort(HTTPStatus.NOT_FOUND)
        return updated.put_into_dto()

    def delete(self, key: int) -> Tuple[Dict[str, str], int]:
        deleted = self._service.delete(key)
        if not deleted:
            abort(HTTPStatus.NOT_FOUND)
        return {"message": f"Record with id={key} successfully deleted"}, HTTPStatus.OK
