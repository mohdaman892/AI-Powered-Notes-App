"""
This module defines the routes for Notes service of the FastAPI App.
"""

from uuid import UUID
from api.v1.notes.controller import NotesController
from core import Response, config, get_session
from fastapi import APIRouter, Depends, Request, Query
from schemas import BaseResponse, CreateNotesSchema, GetNoteResponse, GetAllNotesResponse, UpdateNotesSchema
from sqlalchemy.ext.asyncio import AsyncSession

note_router = APIRouter(prefix="/note")
notes_router = APIRouter(prefix="/notes")


@note_router.post("/", response_model=BaseResponse)
async def create_note(
    data: CreateNotesSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """

    Router method for creating the notes for the logged-in user.

    Args:

        data: Payload containing the notes text.
        request: HTTP request object.
        session: Async DB session.

    Returns:

        HTTP Response containing success message and note_id.
    """
    create_note_response = await NotesController().add_new_note(
        request=request, data=data, session=session
    )
    return Response.success(
        message="Note created Successfully.", status_code=200, body=create_note_response
    )


@note_router.put("/{note_id}", response_model=BaseResponse)
async def update_note(
    note_id: UUID,
    data: UpdateNotesSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """

    Router method for updating the note with the help of note_id.

    Args:

        note_id: UUID of the note.
        data: updated data of the note.
        request: HTTP request object.
        session: Async DB session.

    Returns:

        HTTP Response containing success message and note_id.
    """
    update_note_response = await NotesController().update_note_by_id(
        request=request, note_id=note_id, data=data, session=session
    )
    return Response.success(
        message="Note Updated Successfully.", status_code=200, body=update_note_response
    )


@note_router.get("/{note_id}", response_model=BaseResponse[GetNoteResponse])
async def get_note(
    request: Request,
    note_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """

    Router method for getting the note with note_id.

    Args:

        request: HTTP request object.
        note_id: UUID of the note
        session: Async DB session.

    Returns:

        HTTP Response containing success message and user_id.
    """
    create_note_response = await NotesController().get_note_by_id(
        request=request, note_id=note_id, session=session
    )
    return Response.success(
        message="Note Fetched Successfully.", status_code=200, body=create_note_response
    )


@notes_router.get("/", response_model=BaseResponse[GetAllNotesResponse])
async def show_all_notes(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=6, ge=6, le=20),
    session: AsyncSession = Depends(get_session),
):
    """
    Responsible for fetching all children from the database.

    Args:

        request: Incoming HTTP request object.
        page: The page number to retrieve.
        limit: The number of projects per page.
        session: Async database session for db operations.

    Returns:

        JSON response containing a list of children next page url.
    """
    response = await NotesController().get_all_notes(
        request=request, session=session, page=page, limit=limit
    )
    return Response.success(
        body=response,
        message="Notes retrieved successfully.",
        status_code=200,
    )


@note_router.delete(
    "/{note_id}", response_model=BaseResponse
)
async def delete_child(
    request: Request,
    note_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """
    Responsible for deleting the note with the note_id.

    Args:

        request: Incoming HTTP Request Object
        note_id: UUID.
        session: Async database session for db operations.

    Returns:

        JSON response containing id of the deleted note.
    """
    response = await NotesController().delete_note_with_id(
        request=request, note_id=note_id, session=session
    )
    return Response.success(message="Note Deleted Successfully.", body=response)