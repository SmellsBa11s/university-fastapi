from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.models.enum import SemesterEnum, StatusEnum, LessonTypeEnum


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    course_code: Mapped[str] = mapped_column(nullable=False)
    credits: Mapped[int] = mapped_column(nullable=False)
    instructor_id: Mapped[int] = mapped_column(
        ForeignKey("instructor.id", ondelete="CASCADE"), nullable=False
    )
    semester: Mapped[SemesterEnum] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)


class Enrollment(Base):
    __tablename__ = "enrollment"

    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)
    enrollment_date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[StatusEnum] = mapped_column(nullable=False)


class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    classroom: Mapped[str] = mapped_column(nullable=False)
    lesson_type: Mapped[LessonTypeEnum] = mapped_column(nullable=False)
