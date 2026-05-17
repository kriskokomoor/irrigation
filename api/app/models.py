from pydantic import BaseModel


class ZoneCommand(BaseModel):
    state: str  # "on" or "off"
    source: str | None = None


class TimedZoneCommand(BaseModel):
    source: str | None = None
