from backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ValidationError,
)

from ..constants import ErrorDetails


class LicenseAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.LICENSE_ALREADY_EXISTS


class LicenseNotFoundError(NotFoundError):
    DETAIL = ErrorDetails.LICENSE_NOT_FOUND


class LicenseInactiveError(ValidationError):
    DETAIL = ErrorDetails.LICENSE_INACTIVE


class LicenseExpiredError(ValidationError):
    DETAIL = ErrorDetails.LICENSE_EXPIRED


class LicenseAlreadyInUseError(ValidationError):
    DETAIL = ErrorDetails.LICENSE_ALREADY_IN_USE


class LicenseWrongTenantError(ValidationError):
    DETAIL = ErrorDetails.LICENSE_WRONG_TENANT
