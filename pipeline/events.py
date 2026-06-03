# pipeline/events.py

import uuid
from datetime import datetime


def create_event(
    visitor_id,
    event_type,
    zone_id=None,
    camera_id="CAM1",
    store_id="ST1008",
    confidence=1.0,
    dwell_ms=0,
    is_staff=False,
    metadata=None
):
    """
    Create an event following the challenge schema.
    """

    if metadata is None:
        metadata = {}

    event = {
        "event_id": str(uuid.uuid4()),
        "store_id": store_id,
        "camera_id": camera_id,
        "visitor_id": visitor_id,
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "zone_id": zone_id,
        "dwell_ms": dwell_ms,
        "is_staff": is_staff,
        "confidence": round(confidence, 2),
        "metadata": metadata
    }

    return event


def create_zone_enter_event(
    visitor_id,
    zone_id,
    camera_id="CAM1"
):
    return create_event(
        visitor_id=visitor_id,
        event_type="ZONE_ENTER",
        zone_id=zone_id,
        camera_id=camera_id
    )


def create_zone_exit_event(
    visitor_id,
    zone_id,
    camera_id="CAM1"
):
    return create_event(
        visitor_id=visitor_id,
        event_type="ZONE_EXIT",
        zone_id=zone_id,
        camera_id=camera_id
    )


def create_dwell_event(
    visitor_id,
    zone_id,
    dwell_ms,
    camera_id="CAM1"
):
    return create_event(
        visitor_id=visitor_id,
        event_type="ZONE_DWELL",
        zone_id=zone_id,
        dwell_ms=dwell_ms,
        camera_id=camera_id
    )