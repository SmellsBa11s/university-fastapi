from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class SpecificationBase(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Group(SpecificationBase):
    __tablename__ = "group"


class Faculty(SpecificationBase):
    __tablename__ = "faculty"
