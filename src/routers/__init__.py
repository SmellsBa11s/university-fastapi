from fastapi import APIRouter
from src.routers.auth import router as auth
from src.routers.users import router as users
from src.routers.groups import router as groups

router = APIRouter(prefix="/api")
router.include_router(auth, prefix="/auth", tags=["Authorization"])
router.include_router(users, prefix="/users", tags=["Users"])
router.include_router(groups, prefix="/groups", tags=["Groups"])
