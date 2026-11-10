from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.models import CourseEnrollment


class EnrollmentDAO(GeneralDAO):
    _domain_type = CourseEnrollment
