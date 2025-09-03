
from ..constants import ErrorDetails
from backend.core.exceptions import (
    DetailedHTTPException,
    PreconditionFailedError,
    AlreadyExistsError,
    NotFoundError,
    ValidationError, BadRequestError
)


class TenantAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.TENANT_ALREADY_EXISTS


class TenantNotFoundError(NotFoundError):
    DETAIL = ErrorDetails.TENANT_NOT_FOUND
