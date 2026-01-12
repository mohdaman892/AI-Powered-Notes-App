"""
App wide exception handlers for the application.
This module provides centralized exception handling and standardized error responses
for HTTP exceptions, validation errors, and unexpected runtime errors.
"""

import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .response import Response

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # or DEBUG

if logger.hasHandlers():
    logger.handlers.clear()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] → %(message)s", "%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def http_exception(request: Request, exc: StarletteHTTPException) -> Response:
    """
    Handler for HTTP exceptions thrown by the application
    Args:
        request: The incoming HTTP request
        exc: The HTTP exception that was raised
    Returns:
        Response object with error details
    Note: Local import of logger to avoid circular imports
    """

    logger.error(str(exc))
    return Response(
        status_code=getattr(exc, "status_code", 400),
        content={
            "success": False,
            "message": getattr(exc, "detail", ""),
            "details": "",
        },
    )


def generic_exception(request: Request, exc: Exception) -> Response:
    """
    Handler for any unhandled exceptions in the application
    Args:
        request: The incoming HTTP request
        exc: The exception that was raised
    Returns:
        Response object with generic error message and 500 status code
    Note: Local import of logger to avoid circular imports
    """

    logger.error(str(exc))
    return Response(
        status_code=503,
        content={
            "success": False,
            "message": "We are experiencing high traffic. Kindly try again later.",
            "details": "",
        },
    )


def validation_exception(request: Request, exc: RequestValidationError) -> Response:
    """
    Handler for request validation errors (typically invalid request body/parameters)
    Args:
        request: The incoming HTTP request
        exc: The validation exception containing error details
    Returns:
        Response object with validation error details and 422 status code
    Note: Local import of logger to avoid circular imports
    """

    validation_errors = None
    if hasattr(exc, "errors"):
        validation_errors = exc.errors()[0]
    logger.error(str(exc))
    return Response(
        status_code=422,
        content={
            "success": False,
            "details": "Request validation failed",
            "message": (
                f"""{validation_errors["loc"][1]} {validation_errors["msg"].lower()}"""
                if validation_errors
                else ""
            ),
        },
    )
