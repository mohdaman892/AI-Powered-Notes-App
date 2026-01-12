"""
This module defines the `NotesController` class, which is responsible for all operations regarding notes.
"""

from typing import Any, Dict
from uuid import UUID

from core import setup_logger
from crud import NotesCrud
from fastapi import Request, HTTPException
from models import Note
from schemas import CreateNotesSchema, UpdateNotesSchema
from sqlalchemy.ext.asyncio import AsyncSession

logger = setup_logger()


class NotesController:
    """
      Controller class for handling all operations related to Notes.
    """
    def __init__(self):
        """
          Initializing Constructor method for defining crud variables etc.
        """
        self.notes_crud = NotesCrud()

    async def add_new_note(
        self, *, request: Request, data: CreateNotesSchema, session: AsyncSession
    ) -> Dict[str, Any]:
        """
        Function for handling the creation of a new note.

        Args:
            request: Incoming HTTP request
            data: Note data from the user
            session: Async DB session

        Returns:
            Create Notes Response Dictionary

        """
        logger.info("Inside Notes Controller, Creating a new Note")

        current_user_id = request.state.session_data.get("user_id")
        data.user_id = current_user_id
        notes_obj = await self.notes_crud.insert(
            session=session, create_obj=data, unique_identifier=current_user_id
        )
        create_notes_response = {"id": notes_obj.id, "user_id": data.user_id}
        return create_notes_response

    async def get_note_by_id(
        self, *, request: Request, note_id: UUID, session: AsyncSession
    ) -> Dict[str, Any]:
        """
        Function for fetching the details of a note by its note_id

        Args:
            request: Incoming HTTP request
            note_id: UUID of the note
            session: Async DB session

        Returns:
            Cookies dict and Dictionary Response

        """
        logger.info("Inside Notes Controller, fetching details of a Note")

        notes_obj = await self.notes_crud.get(
            session=session, field=Note.id, value=note_id
        )
        if not notes_obj:
            logger.info("Note with provided ID does not exists")
            raise HTTPException(
                status_code=404, detail="Note with provided ID does not exists"
            )
        get_note_response = notes_obj.to_dict()
        return get_note_response

    async def update_note_by_id(
        self, *, request: Request, note_id: UUID, data: UpdateNotesSchema, session: AsyncSession
    ) -> Dict[str, Any]:
        """
        Function for handling the update note action with the help of its note_id

        Args:
            request: Incoming HTTP request
            data: Updated data of the note.
            note_id: UUID of the note
            session: Async DB session

        Returns:
            Update Notes Response Dictionary

        """
        logger.info("Inside Notes Controller, Updating a Note")

        current_user_id = request.state.session_data.get("user_id")

        notes_obj = await self.notes_crud.get(
            session=session, field=Note.id, value=note_id
        )
        if not notes_obj:
            logger.info("Note with provided ID does not exists")
            raise HTTPException(
                status_code=404, detail="Note with provided ID does not exists"
            )
        data_to_update = {
            "text": data.text,
            "user_id": notes_obj.user_id
        }
        updated_obj = await self.notes_crud.update(
            session=session,
            db_obj=notes_obj,
            obj_in=data_to_update,
            unique_identifier=current_user_id
        )
        update_notes_response = {"id": updated_obj.id}
        return update_notes_response

    async def get_all_notes(
        self, *, request: Request, session: AsyncSession, page: int, limit: int
    ) -> Dict[str, Any]:
        """

        Fetches all notes from database with pagination.
        Args:
            request: Incoming HTTP request object.
            session: Async database session for db operations.
            page: The page number to fetch, starting from 1.
            limit: The maximum number of children to return per page.
        Returns:
            notes_data: List of notes and next page endpoint.
        """
        logger.info("Inside NotesController fetching all the notes ...")
        offset = (page - 1) * limit
        notes = await self.notes_crud.get_multi(
            session=session, skip=offset, limit=limit + 1
        )
        notes_list = []
        for note in notes:
            notes_summary_data = {
                "id": note.id,
                "text": note.text,
                "user_id": note.user_id,
                "created_at": note.created_at.isoformat(),
                "updated_at": note.updated_at.isoformat(),
            }
            notes_list.append(notes_summary_data)
        next_page_url = (
            None
            if not len(notes) > limit
            else f"{request.url.path}?page={page + 1}&limit={limit}"
        )
        notes_data = {"notes": notes_list, "next_page_url": next_page_url}
        return notes_data

    async def delete_note_with_id(self, *, request: Request, note_id: UUID, session: AsyncSession):
        """
        Soft deletes the note with the given ID.
        Args:
            request: Incoming HTTP Request Object
            session: Async database session for db operations.
            note_id: The ID of the note to delete.
        Returns:
            deleted_note_data: Dictionary containing deleted note ID.
        """
        logger.info("Inside Children Controller, Deleting Child Data with Child ID.")
        current_user_id = request.state.session_data.get("user_id")

        notes_obj = await self.notes_crud.get(
            session=session, field=Note.id, value=note_id
        )
        if not notes_obj:
            logger.info("Note with provided ID does not exists")
            raise HTTPException(
                status_code=404, detail="Note with provided ID does not exists"
            )

        deleted_note = await self.notes_crud.delete(
            session=session, db_obj=notes_obj, unique_identifier=current_user_id
        )
        deleted_note_data = {"id": deleted_note.id}
        return deleted_note_data
