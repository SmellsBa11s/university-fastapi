from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.models.base import Base
from datetime import datetime

from src.models.enum import UserRoleEnum


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    user_role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.ADMIN)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(default=True)


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    student_number: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE"), nullable=False
    )
    enrollment_year: Mapped[int] = mapped_column(nullable=False)
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculty.id", ondelete="CASCADE"), nullable=False
    )


class Instructor(Base):
    __tablename__ = "instructor"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[str] = mapped_column(nullable=False)
    department: Mapped[str] = mapped_column(nullable=False)
    academic_degree: Mapped[str] = mapped_column(nullable=False)
