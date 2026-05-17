from threading import Lock, Timer

from fastapi import APIRouter, Body, HTTPException

from ..models import TimedZoneCommand, ZoneCommand
from ..devices import set_zone, get_status
from ..event_log import log_irrigation_event

router = APIRouter()

TEN_MINUTES_SECONDS = 10 * 60
scheduled_off_timers: dict[int, Timer] = {}
scheduled_off_lock = Lock()


def response_details(source: str, controller_response: str | None = None):
    details = f"source={source}"
    if controller_response is not None:
        details = f"{details}; controller_response={controller_response}"
    return details


def turn_zone_off(zone_id: int):
    try:
        result = set_zone(zone_id, "off")
        log_irrigation_event(
            zone_id,
            "10_min_default_off",
            True,
            response_body=result,
        )
    except Exception as exc:
        log_irrigation_event(
            zone_id,
            "10_min_default_off",
            False,
            error_message=str(exc),
        )
        raise
    finally:
        cancel_scheduled_off(zone_id)


def cancel_scheduled_off(zone_id: int):
    with scheduled_off_lock:
        timer = scheduled_off_timers.pop(zone_id, None)
    if timer:
        timer.cancel()
    return timer is not None


def schedule_zone_off(zone_id: int, delay_seconds: int):
    replaced_existing_timer = cancel_scheduled_off(zone_id)
    timer = Timer(delay_seconds, turn_zone_off, args=(zone_id,))
    timer.daemon = True
    with scheduled_off_lock:
        scheduled_off_timers[zone_id] = timer
    timer.start()
    return replaced_existing_timer


@router.post("/valve/{zone_id}")
def control_valve(zone_id: int, cmd: ZoneCommand):
    source = cmd.source or "api"
    try:
        if cancel_scheduled_off(zone_id):
            log_irrigation_event(
                zone_id,
                "10_min_cancelled_manual_command",
                True,
                response_body=(
                    f"requested_state={cmd.state}; "
                    f"{response_details(source)}"
                ),
            )
        result = set_zone(zone_id, cmd.state)
        log_irrigation_event(
            zone_id,
            cmd.state,
            True,
            response_body=response_details(source, result),
        )
        return {"result": result}
    except Exception as e:
        log_irrigation_event(
            zone_id,
            cmd.state,
            False,
            response_body=response_details(source),
            error_message=str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/valve/{zone_id}/10-min")
def run_valve_for_ten_minutes(
    zone_id: int,
    cmd: TimedZoneCommand | None = Body(default=None),
):
    source = cmd.source if cmd and cmd.source else "api"
    try:
        result = set_zone(zone_id, "on")
        if schedule_zone_off(zone_id, TEN_MINUTES_SECONDS):
            log_irrigation_event(
                zone_id,
                "10_min_cancelled_rescheduled",
                True,
                response_body=response_details(source),
            )
        log_irrigation_event(
            zone_id,
            "10_min_started",
            True,
            response_body=(
                f"duration_seconds={TEN_MINUTES_SECONDS}; "
                f"default_off_scheduled=true; "
                f"{response_details(source, result)}"
            ),
        )
        return {"result": result, "scheduled_off_seconds": TEN_MINUTES_SECONDS}
    except Exception as e:
        log_irrigation_event(
            zone_id,
            "10_min_started",
            False,
            response_body=(
                f"duration_seconds={TEN_MINUTES_SECONDS}; "
                f"{response_details(source)}"
            ),
            error_message=str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
def status():
    return get_status()
