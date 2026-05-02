from pydantic import BaseModel

class ZoneCommand(BaseModel):
    state: str  # "on" or "off"