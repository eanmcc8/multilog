class MLXError(Exception):
    """Base Multilogin X API error."""

    def __init__(self, message: str, status_code: int | None = None, payload: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}


class MLXAuthError(MLXError):
    pass


class MLXAPIError(MLXError):
    pass
