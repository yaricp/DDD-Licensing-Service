from backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ValidationError,
)

from ..constants import ErrorDetails


class SubdivisionAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.SUBDIVISION_ALREADY_EXISTS


class SubdivisionNotFoundError(NotFoundError):
    DETAIL = ErrorDetails.SUBDIVISION_NOT_FOUND


class SubdivisionInactiveError(ValidationError):
    DETAIL = ErrorDetails.SUBDIVISION_INACTIVE
