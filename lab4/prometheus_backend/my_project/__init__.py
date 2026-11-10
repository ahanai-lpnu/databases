import os
import yaml
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)

    config_path = os.path.join(os.path.dirname(__file__), "../config/app.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)

    app.config.update(config_data.get("flask", {}))
    app.json.ensure_ascii = False

    db.init_app(app)

    from my_project.auth.route import register_routes
    register_routes(app)

    @app.get("/")
    def index():
        return {
            "status": "Prometheus DB API is running",
            "endpoints": [
                "/api/users",
                "/api/users/with-courses",
                "/api/categories",
                "/api/categories/with-courses",
                "/api/courses",
                "/api/courses/with-modules",
                "/api/courses/with-students",
                "/api/modules",
                "/api/enrollments",
            ],
        }

    return app
