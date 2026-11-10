from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.models import Category


class CategoryDAO(GeneralDAO):
    _domain_type = Category
