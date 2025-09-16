from backend.core.exceptions import (
    AlreadyExistsError,
)

from ..constants import ErrorDetails


class SubdivisionStatisticAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.SUBDIVISION_STATISTIC_ALREADY_EXISTS
