"""
All schemas related to notes
"""

from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class CreateNotesSchema(BaseModel):
    """Schema for Creating a New Note"""
    text: str
    user_id: Optional[UUID] = None


class UpdateNotesSchema(CreateNotesSchema):
    """Schema for Updating a Note"""


class GetNoteResponse(BaseModel):
    """Response Schema for Get Note"""
    text: str
    user_id: Optional[UUID] = None


class GetAllNotesResponse(BaseModel):
    """Response Schema for Get All Notes"""
    notes: List[GetNoteResponse]
    next_page_url: Optional[str]
