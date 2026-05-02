from fastapi import APIRouter, HTTPException
from ..models import ZoneCommand
from ..devices import set_zone, get_status

router = APIRouter()

@router.post("/valve/{zone_id}")
def control_valve(zone_id: int, cmd: ZoneCommand):
    try:
        result = set_zone(zone_id, cmd.state)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
def status():
    return get_status()
