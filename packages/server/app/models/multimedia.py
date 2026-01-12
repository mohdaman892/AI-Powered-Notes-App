from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, VARCHAR

from .base import Base


class Multimedia(Base):
    """
    Represents multimedia attached to a note:
    audio, video, and images.
    """

    __tablename__ = "multimedia"

    # 🔗 Which note this belongs to
    note_id: Mapped[str] = mapped_column(
        ForeignKey("notes.id"),
        nullable=False,
    )

    # 🔗 Which user owns this multimedia (same as note.user_id)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # 🎧 Audio file (S3 URL or similar)
    audio_url: Mapped[Optional[str]] = mapped_column(
        VARCHAR(500),
        nullable=True,
    )

    # 🎥 Video file (S3 URL or similar)
    video_url: Mapped[Optional[str]] = mapped_column(
        VARCHAR(500),
        nullable=True,
    )

    # 🖼️ Multiple image URLs stored as JSON array
    images: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
    )

    # # 🔁 Relationships
    #
    # # Many multimedia rows → one note
    # note: Mapped["Note"] = relationship(
    #     back_populates="multimedia_items",
    # )
    #
    # # Many multimedia rows → one user
    # user: Mapped["User"] = relationship(
    #     back_populates="multimedia_items",
    # )
