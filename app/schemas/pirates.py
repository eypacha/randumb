from pydantic import BaseModel

class Pirate(BaseModel):
    id: int | None = None
    text: str
