from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.models import Course


class CourseDAO(GeneralDAO):
    _domain_type = Course
