from my_project.auth.dao import enrollment_dao
from my_project.auth.service.general_service import GeneralService


class EnrollmentService(GeneralService):
    _dao = enrollment_dao
