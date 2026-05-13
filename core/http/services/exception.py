class APIError(Exception):
    """Base API exception."""

class ClientError(APIError):
    """4xx client-side HTTP errors."""

class UnauthorizedError(ClientError):
    """401 Unauthorized."""

class ForbiddenError(ClientError):
    """403 Forbidden."""

class NotFoundError(ClientError):
    """404 Not Found."""

class ValidationError(ClientError):
    """422 Validation Error."""

class ConflictError(ClientError):
    """409 Conflict."""

class ServerError(APIError):
    """5xx server-side HTTP errors."""

class ServiceUnavailableError(ServerError):
    """503 Service Unavailable."""

class NetworkError(APIError):
    """Network or connection error."""

class RetryExceededError(NetworkError):
    """Retry attempts exceeded."""