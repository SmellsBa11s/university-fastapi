from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.models.enum import TypeEnum


class NewsEvent(Base):
    __tablename__ = "news_event"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    publish_date: Mapped[datetime] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[TypeEnum] = mapped_column(nullable=False)
    event_date: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
