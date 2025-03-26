from src.crud.base import BaseDAO
from src.models import Schedule


class ScheduleDAO(BaseDAO):
    """Data Access Object (DAO) for managing schedules in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the Schedule entity.

    Usage examples:
        schedule_dao = ScheduleDAO()
        new_schedule = await schedule_dao.add({
                "course_id": 1,
                "group_id": 1,
                "day_of_week": "Monday",
                "start_time": "09:00",
                "end_time": "10:30",
                "room": "101"
            })
        found_schedule = await schedule_dao.find_one_or_none(
            course_id=1, group_id=1, day_of_week="Monday"
        )

    Attributes:
        model (Schedule): SQLAlchemy Schedule model used for operations
    """

    model = Schedule
