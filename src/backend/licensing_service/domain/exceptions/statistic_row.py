from ..constants import ErrorDetails
from backend.core.exceptions import (
    DetailedHTTPException,
    PreconditionFailedError,
    AlreadyExistsError,
    NotFoundError,
    ValidationError, BadRequestError
)


class SubdivisionStatisticAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.SUBDIVISION_STATISTIC_ALREADY_EXISTS
