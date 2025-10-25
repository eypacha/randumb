from pydantic import BaseModel, Field
from uuid import UUID


class PirateLangOutSingle(BaseModel):
    id: UUID
    text: str
    lang: str


class PirateLangOut(BaseModel):
    id: UUID
    text: str
    lang: str


class PirateCreate(BaseModel):
    text: str
    lang: str = Field(..., example="en")


class Pirate(BaseModel):
    id: UUID
    text: str
    lang: str
