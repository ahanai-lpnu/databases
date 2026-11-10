from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service import enrollment_service


class EnrollmentController(GeneralController):
    _service = enrollment_service
