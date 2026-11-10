from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.models import Module


class ModuleDAO(GeneralDAO):
    _domain_type = Module
