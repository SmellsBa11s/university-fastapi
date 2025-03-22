from fastapi import APIRouter
from src.routers.auth import router as auth


router = APIRouter(prefix="/api")
router.include_router(auth, prefix="/auth", tags=["Authorization"])
