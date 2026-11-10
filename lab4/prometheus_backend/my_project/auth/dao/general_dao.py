from abc import ABC
from typing import List, Optional, Type
from my_project import db


class GeneralDAO(ABC):
    _domain_type: Type[db.Model]

    def find_all(self) -> List[object]:
        return db.session.query(self._domain_type).all()

    def find_by_id(self, key: int) -> Optional[object]:
        return db.session.get(self._domain_type, key)

    def create(self, obj: object) -> object:
        db.session.add(obj)
        db.session.commit()
        return obj

    def update(self, key: int, in_obj: object) -> Optional[object]:
        domain_obj = db.session.get(self._domain_type, key)
        if not domain_obj:
            return None
        mapper = db.inspect(self._domain_type)
        for column in mapper.columns:
            if not column.primary_key:
                val = getattr(in_obj, column.key)
                if val is not None:
                    setattr(domain_obj, column.key, val)
        db.session.commit()
        return domain_obj

    def delete(self, key: int) -> bool:
        domain_obj = db.session.get(self._domain_type, key)
        if not domain_obj:
            return False
        db.session.delete(domain_obj)
        db.session.commit()
        return True
