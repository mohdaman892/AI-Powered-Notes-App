from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TEXT

from .base import Base


class Note(Base):
    """
    Represents a text note created by a user.
    """

    __tablename__ = "notes"

    # 🔗 Which user owns this note
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # 📝 Note content
    text: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )

    # # 🔁 Relationships
    #
    # # Many notes → one user
    # user: Mapped["User"] = relationship(
    #     back_populates="notes",
    # )
    #
    # # One note → many multimedia attachments
    # multimedia_items: Mapped[list["Multimedia"]] = relationship(
    #     back_populates="note",
    #     cascade="all, delete-orphan",
    # )
