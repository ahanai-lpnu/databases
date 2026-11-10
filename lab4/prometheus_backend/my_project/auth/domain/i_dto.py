from typing import Any, Dict


class IDto:
    def put_into_dto(self) -> Dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> object:
        raise NotImplementedError