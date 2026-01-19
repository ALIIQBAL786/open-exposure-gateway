from pydantic import BaseModel


class ErrorInfo(BaseModel):
    status: int  # HTTP status code
    code: str  # error code, e.g. UNAVAILABLE, INTERNAL, NOT_FOUND, PERMISSION_DENIED,
    message: str
