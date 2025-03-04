from pydantic import BaseModel, field_validator, ValidationError
from errors import HttpError

class CreateAdvertisment(BaseModel):
    Title: str
    Body: str
    Owner: str



class UpdateAdvertisment(BaseModel):
    Title: str | None = None
    Body: str | None = None
    Owner: str | None = None

SCHEMA = type[CreateAdvertisment] | type[UpdateAdvertisment]

def validate(cls_schema: SCHEMA, json_data: dict):
    try:
        schema = cls_schema(**json_data)
        return schema.dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)
