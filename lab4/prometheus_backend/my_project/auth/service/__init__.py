from .orders.category_service import CategoryService
from .orders.course_service import CourseService
from .orders.user_service import UserService
from .orders.module_service import ModuleService
from .orders.enrollment_service import EnrollmentService

category_service = CategoryService()
course_service = CourseService()
user_service = UserService()
module_service = ModuleService()
enrollment_service = EnrollmentService()
