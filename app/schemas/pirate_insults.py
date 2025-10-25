from pydantic import BaseModel

class PirateInsult(BaseModel):
    id: int | None = None
    text: str
