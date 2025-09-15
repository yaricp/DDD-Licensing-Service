from backend.core.constants import ErrorDetails as BaseErrorDetails
# from src.users.config import UserValidationConfig


class ErrorDetails(BaseErrorDetails):
    """
    Authorization and authentication error messages for custom exceptions.
    """

    TENANT_ALREADY_EXISTS: str = "Tenant with provided credentials already exists"
    TENANT_NOT_FOUND: str = "Tenant with provided credentials not found"
    TENANT_ATTRIBUTE_REQUIRED: str = "Tenant id, email or username is required"
    TENANT_CAN_NOT_VOTE_FOR_HIMSELF: str = "Tenant can not vote for himself"
    TENANT_STATISTICS_NOT_FOUND: str = "Tenant statistics not found"

    LICENSE_ALREADY_EXISTS: str = "License with provided credentials already exists"
    LICENSE_NOT_FOUND: str = "License with provided credentials not found"
    LICENSE_ATTRIBUTE_REQUIRED: str = "License id, email or username is required"
    LICENSE_CAN_NOT_VOTE_FOR_HIMSELF: str = "License can not vote for himself"
    LICENSE_INACTIVE: str = "License is inactive"
    LICENSE_EXPIRED: str = "License is expired"
    LICENSE_ALREADY_IN_USE: str = "License already in use"
    LICENSE_WRONG_TENANT: str = "Wrong Tenant of Subdivision"

    SUBDIVISION_ALREADY_EXISTS: str = "Subdivision with provided credentials already exists"
    SUBDIVISION_NOT_FOUND: str = "Subdivision with provided credentials not found"
    SUBDIVISION_ATTRIBUTE_REQUIRED: str = "Subdivision id, email or username is required"
    SUBDIVISION_CAN_NOT_VOTE_FOR_HIMSELF: str = "User can not vote for himself"
    SUBDIVISION_STATISTICS_NOT_FOUND: str = "Subdivision statistics not found"
    SUBDIVISION_ALREADY_VOTED: str = "Current user already voted for provided user"
    SUBDIVISION_INACTIVE: str = "Subdivision is inactive"

    SUBDIVISION_STATISTIC_ALREADY_EXISTS: str = "Subdivision Statistic Row already exists"

    # USER_ALREADY_EXISTS: str = "User with provided credentials already exists"
    # USER_NOT_FOUND: str = "User with provided credentials not found"
    # USER_ATTRIBUTE_REQUIRED: str = "user id, email or username is required"
    # USER_CAN_NOT_VOTE_FOR_HIMSELF: str = "User can not vote for himself"
    # USER_STATISTICS_NOT_FOUND: str = "User statistics not found"
    # USER_ALREADY_VOTED: str = "Current user already voted for provided user"