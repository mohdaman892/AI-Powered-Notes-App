"""
This module defines a generic `BaseCrud` class that provides common CRUD operations
for any SQLAlchemy model. It includes methods for retrieving, creating, updating,
and deleting records in the database, with support for soft deletion.

The `BaseCrud` class is designed to work with any model that inherits from the `Base`
class and includes an `is_deleted` field for soft deletion.
"""


class BaseCrud:
    pass
