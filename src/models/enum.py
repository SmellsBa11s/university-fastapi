from enum import Enum


class TypeEnum(Enum):
    NEWS = "news"
    EVENT = "event"


class SemesterEnum(Enum):
    AUTUMN = "autumn"
    SPRING = "spring"


class UserRoleEnum(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    INSTRUCTOR = "instructor"


class StatusEnum(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"


class LessonTypeEnum(Enum):
    LECTURE = "lecture"
    PRACTICE = "practice"
    LAB = "lab"
