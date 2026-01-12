"""
Module defines a `NotesCrud` by inheriting the `BaseCrud` to add CRUD operation
for the `Notes` model.
"""

from models import Note
from schemas import CreateNotesSchema

from .base import BaseCrud


class NotesCrud(BaseCrud[Note, CreateNotesSchema, CreateNotesSchema]):
    """
    This class is responsible for all CRUD operations for the `Notes` model.
    """

    def __init__(self):
        """
        Initializes the ChildrenCrud instance with the `Children` model.
        """
        super().__init__(model=Note)
