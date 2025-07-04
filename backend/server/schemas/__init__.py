from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_serializer


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        use_enum_values=True,
        alias_generator=str.lower,
    )

    @field_serializer(datetime, when_used="json", check_fields=False)
    def serialize_datetime(cls, v: datetime) -> str:
        return v.astimezone(timezone.utc).isoformat()


class BaseRequestSchema(BaseSchema):
    model_config = ConfigDict(extra="forbid")


class BaseResponseSchema(BaseSchema):
    pass
