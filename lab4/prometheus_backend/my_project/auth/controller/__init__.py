from .orders.category_controller import CategoryController
from .orders.course_controller import CourseController
from .orders.user_controller import UserController
from .orders.module_controller import ModuleController
from .orders.enrollment_controller import EnrollmentController

category_controller = CategoryController()
course_controller = CourseController()
user_controller = UserController()
module_controller = ModuleController()
enrollment_controller = EnrollmentController()
