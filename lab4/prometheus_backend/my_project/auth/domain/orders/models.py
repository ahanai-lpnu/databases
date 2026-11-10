from __future__ import annotations
from datetime import datetime
from typing import Any, Dict
from my_project import db
from my_project.auth.domain.i_dto import IDto


class User(db.Model, IDto):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("student", "instructor", "admin"), default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    authored_courses = db.relationship("Course", back_populates="author", lazy="select")
    enrollments = db.relationship("CourseEnrollment", back_populates="student", cascade="all, delete-orphan")
    notifications = db.relationship("SystemNotification", back_populates="student", cascade="all, delete-orphan")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "profile": self.profile.put_into_dto() if self.profile else None,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> User:
        return User(
            first_name=dto_dict.get("first_name"),
            last_name=dto_dict.get("last_name"),
            email=dto_dict.get("email"),
            password_hash=dto_dict.get("password_hash", "default_hash"),
            role=dto_dict.get("role", "student"),
        )


class UserProfile(db.Model, IDto):
    __tablename__ = "user_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    phone_number = db.Column(db.String(20), unique=True)
    bio = db.Column(db.Text)
    timezone = db.Column(db.String(50), default="Europe/Kyiv")
    receive_email_alerts = db.Column(db.Boolean, default=True)

    user = db.relationship("User", back_populates="profile")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "phone_number": self.phone_number,
            "bio": self.bio,
            "timezone": self.timezone,
            "receive_email_alerts": self.receive_email_alerts,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> UserProfile:
        return UserProfile(
            user_id=dto_dict.get("user_id"),
            phone_number=dto_dict.get("phone_number"),
            bio=dto_dict.get("bio"),
            timezone=dto_dict.get("timezone", "Europe/Kyiv"),
            receive_email_alerts=dto_dict.get("receive_email_alerts", True),
        )


class Category(db.Model, IDto):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))

    courses = db.relationship("Course", back_populates="category", lazy="select")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Category:
        return Category(
            name=dto_dict.get("name"),
            description=dto_dict.get("description"),
        )


class Course(db.Model, IDto):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    expected_duration_days = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship("Category", back_populates="courses")
    author = db.relationship("User", back_populates="authored_courses")
    modules = db.relationship("Module", back_populates="course", cascade="all, delete-orphan")
    enrollments = db.relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "author_id": self.author_id,
            "author_name": f"{self.author.first_name} {self.author.last_name}" if self.author else None,
            "title": self.title,
            "description": self.description,
            "expected_duration_days": self.expected_duration_days,
            "is_published": self.is_published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Course:
        return Course(
            category_id=dto_dict.get("category_id"),
            author_id=dto_dict.get("author_id"),
            title=dto_dict.get("title"),
            description=dto_dict.get("description"),
            expected_duration_days=dto_dict.get("expected_duration_days", 30),
            is_published=dto_dict.get("is_published", False),
        )


class CourseEnrollment(db.Model, IDto):
    __tablename__ = "course_enrollments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    expected_completion_date = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum("active", "completed", "behind_schedule", "dropped"), default="active")

    student = db.relationship("User", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": f"{self.student.first_name} {self.student.last_name}" if self.student else None,
            "course_id": self.course_id,
            "course_title": self.course.title if self.course else None,
            "enrolled_at": self.enrolled_at.isoformat() if self.enrolled_at else None,
            "expected_completion_date": self.expected_completion_date.isoformat() if self.expected_completion_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> CourseEnrollment:
        exp_date = dto_dict.get("expected_completion_date")
        if isinstance(exp_date, str):
            exp_date = datetime.fromisoformat(exp_date)
        return CourseEnrollment(
            student_id=dto_dict.get("student_id"),
            course_id=dto_dict.get("course_id"),
            expected_completion_date=exp_date or datetime.utcnow(),
            status=dto_dict.get("status", "active"),
        )


class Module(db.Model, IDto):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    recommended_days_to_complete = db.Column(db.Integer, default=7)

    course = db.relationship("Course", back_populates="modules")
    tests = db.relationship("Test", back_populates="module", cascade="all, delete-orphan")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "course_id": self.course_id,
            "course_title": self.course.title if self.course else None,
            "title": self.title,
            "description": self.description,
            "order_index": self.order_index,
            "recommended_days_to_complete": self.recommended_days_to_complete,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Module:
        return Module(
            course_id=dto_dict.get("course_id"),
            title=dto_dict.get("title"),
            description=dto_dict.get("description"),
            order_index=dto_dict.get("order_index", 1),
            recommended_days_to_complete=dto_dict.get("recommended_days_to_complete", 7),
        )


class ModuleProgress(db.Model, IDto):
    __tablename__ = "module_progress"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("course_enrollments.id", ondelete="CASCADE"), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "enrollment_id": self.enrollment_id,
            "module_id": self.module_id,
            "is_completed": self.is_completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> ModuleProgress:
        return ModuleProgress(
            enrollment_id=dto_dict.get("enrollment_id"),
            module_id=dto_dict.get("module_id"),
            is_completed=dto_dict.get("is_completed", False),
        )


class SystemNotification(db.Model, IDto):
    __tablename__ = "system_notifications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    notification_type = db.Column(
        db.Enum("schedule_delay", "deadline_warning", "course_completed"), default="schedule_delay"
    )
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", back_populates="notifications")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "notification_type": self.notification_type,
            "message": self.message,
            "is_read": self.is_read,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> SystemNotification:
        return SystemNotification(
            student_id=dto_dict.get("student_id"),
            course_id=dto_dict.get("course_id"),
            notification_type=dto_dict.get("notification_type", "schedule_delay"),
            message=dto_dict.get("message"),
            is_read=dto_dict.get("is_read", False),
        )


class Test(db.Model, IDto):
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    max_score = db.Column(db.Integer, default=100)
    passing_score = db.Column(db.Integer, default=60)

    module = db.relationship("Module", back_populates="tests")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "module_id": self.module_id,
            "title": self.title,
            "max_score": self.max_score,
            "passing_score": self.passing_score,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Test:
        return Test(
            module_id=dto_dict.get("module_id"),
            title=dto_dict.get("title"),
            max_score=dto_dict.get("max_score", 100),
            passing_score=dto_dict.get("passing_score", 60),
        )
