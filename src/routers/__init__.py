from fastapi import APIRouter
from src.routers.auth import router as auth
from src.routers.users import router as users
from src.routers.groups import router as groups
from src.routers.faculty import router as faculty
from src.routers.students import router as students
from src.routers.instructors import router as instructors

router = APIRouter(prefix="/api")
router.include_router(auth, prefix="/auth", tags=["Authorization"])
router.include_router(users, prefix="/users", tags=["Users"])
router.include_router(groups, prefix="/groups", tags=["Groups"])
router.include_router(faculty, prefix="/faculty", tags=["Faculty"])
router.include_router(students, prefix="/students", tags=["Students"])
router.include_router(instructors, prefix="/instructors", tags=["Instructors"])
