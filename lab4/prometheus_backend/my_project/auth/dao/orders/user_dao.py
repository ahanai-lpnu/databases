from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.models import User


class UserDAO(GeneralDAO):
    _domain_type = User
