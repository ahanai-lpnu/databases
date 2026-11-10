from .orders.category_dao import CategoryDAO
from .orders.course_dao import CourseDAO
from .orders.user_dao import UserDAO
from .orders.module_dao import ModuleDAO
from .orders.enrollment_dao import EnrollmentDAO

category_dao = CategoryDAO()
course_dao = CourseDAO()
user_dao = UserDAO()
module_dao = ModuleDAO()
enrollment_dao = EnrollmentDAO()
