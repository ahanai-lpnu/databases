from flask import Flask
from .error_handler import err_handler_bp
from .orders.category_route import category_bp
from .orders.course_route import course_bp
from .orders.user_route import user_bp
from .orders.module_route import module_bp
from .orders.enrollment_route import enrollment_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(err_handler_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(module_bp)
    app.register_blueprint(enrollment_bp)
