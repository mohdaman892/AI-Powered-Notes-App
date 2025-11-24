from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import VARCHAR

from app.models.base import Base


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    """
    Represents a user in the system.
    Inherits audit + id fields from Base.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True,
        nullable=False,
    )

    role: Mapped[Role] = mapped_column(
        VARCHAR(20),
        default=Role.USER,
        nullable=False,
    )

    _password: Mapped[str] = mapped_column(
        "password",
        VARCHAR(255),
        nullable=False,
    )

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, raw_password: str):
        # TODO: hash inside this setter
        self._password = raw_password




    # notes: Mapped[list["Note"]] = relationship(
    #     back_populates="user",
    #     cascade="all, delete-orphan",
    # )
    #
    # multimedia_items: Mapped[list["Multimedia"]] = relationship(
    #     back_populates="user",
    #     cascade="all, delete-orphan",
    # )
