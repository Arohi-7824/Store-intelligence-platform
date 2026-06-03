from datetime import datetime
from events import create_dwell_event

# Stores when a visitor entered a zone
zone_entry_times = {}


def record_zone_entry(visitor_id, zone_id):
    """
    Called whenever a visitor enters a zone.
    """

    zone_entry_times[(visitor_id, zone_id)] = datetime.utcnow()


def process_zone_exit(visitor_id, zone_id):
    """
    Called whenever a visitor exits a zone.
    Returns a ZONE_DWELL event.
    """

    key = (visitor_id, zone_id)

    if key not in zone_entry_times:
        return None

    entry_time = zone_entry_times.pop(key)

    dwell_ms = int(
        (datetime.utcnow() - entry_time).total_seconds() * 1000
    )

    event = create_dwell_event(
        visitor_id=visitor_id,
        zone_id=zone_id,
        dwell_ms=dwell_ms
    )

    return event