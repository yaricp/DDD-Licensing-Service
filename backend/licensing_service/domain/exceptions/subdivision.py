
from ..constants import ErrorDetails
from backend.core.exceptions import (
    DetailedHTTPException,
    PreconditionFailedError,
    AlreadyExistsError,
    NotFoundError,
    ValidationError, BadRequestError
)


class SubdivisionAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.SUBDIVISION_ALREADY_EXISTS


class SubdivisionNotFoundError(NotFoundError):
    DETAIL = ErrorDetails.SUBDIVISION_NOT_FOUND


class SubdivisionInactiveError(ValidationError):
    DETAIL = ErrorDetails.SUBDIVISION_INACTIVE
