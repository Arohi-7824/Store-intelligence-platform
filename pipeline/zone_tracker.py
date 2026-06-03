from events import (
    create_zone_enter_event,
    create_zone_exit_event
)
from dwell_tracker import process_zone_exit, record_zone_entry

visitor_last_zone = {}

# candidate zone waiting for confirmation
candidate_zone = {}

# how many consecutive frames seen in candidate zone
candidate_count = {}

MIN_STABLE_FRAMES = 15


def process_zone_change(visitor_id, current_zone):

    events = []

    previous_zone = visitor_last_zone.get(visitor_id)

    # first observation
    if previous_zone is None:

        visitor_last_zone[visitor_id] = current_zone

        record_zone_entry(
            f"VIS_{visitor_id}",
            current_zone
        )

        events.append(
            create_zone_enter_event(
                visitor_id=f"VIS_{visitor_id}",
                zone_id=current_zone
            )
        )

        return events

    # still in same zone
    if current_zone == previous_zone:

        candidate_zone.pop(visitor_id, None)
        candidate_count.pop(visitor_id, None)

        return events

    # possible transition
    if visitor_id not in candidate_zone:

        candidate_zone[visitor_id] = current_zone
        candidate_count[visitor_id] = 1

        return events

    # different candidate appeared
    if candidate_zone[visitor_id] != current_zone:

        candidate_zone[visitor_id] = current_zone
        candidate_count[visitor_id] = 1

        return events

    # same candidate continues
    candidate_count[visitor_id] += 1

    print(
    f"VIS_{visitor_id} "
    f"candidate={current_zone} "
    f"count={candidate_count[visitor_id]}"
)

    # accept zone change only after stability
    if candidate_count[visitor_id] >= MIN_STABLE_FRAMES:

        dwell_event = process_zone_exit(
            f"VIS_{visitor_id}",
            previous_zone
        )

        if dwell_event:
            events.append(dwell_event)

        events.append(
            create_zone_exit_event(
                visitor_id=f"VIS_{visitor_id}",
                zone_id=previous_zone
            )
        )
        record_zone_entry(
            f"VIS_{visitor_id}",
            current_zone
        )

        events.append(
            create_zone_enter_event(
                visitor_id=f"VIS_{visitor_id}",
                zone_id=current_zone
            )
        )

        visitor_last_zone[visitor_id] = current_zone

        candidate_zone.pop(visitor_id, None)
        candidate_count.pop(visitor_id, None)

    return events