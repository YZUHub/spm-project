from pydantic import Field

from server.schemas import BaseResponseSchema


class CountResponse(BaseResponseSchema):
    count: int = Field(..., description="Number of items")


class StatusResponse(BaseResponseSchema):
    success: str = Field(..., description="Status of the request")
    message: str | None = Field(None, description="Message from the server")
