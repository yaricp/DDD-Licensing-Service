from backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
)

from ..constants import ErrorDetails


class TenantAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.TENANT_ALREADY_EXISTS


class TenantNotFoundError(NotFoundError):
    DETAIL = ErrorDetails.TENANT_NOT_FOUND
