from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service import module_service


class ModuleController(GeneralController):
    _service = module_service
