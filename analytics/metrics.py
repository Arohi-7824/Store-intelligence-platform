import json
from collections import Counter


def load_events(path):

    events = []

    with open(path, "r") as f:

        for line in f:
            events.append(json.loads(line))

    return events


def get_metrics(path):

    events = load_events(path)

    visitors = set()

    dwell_times = []

    zone_counter = Counter()

    for event in events:

        visitors.add(event["visitor_id"])

        if event["event_type"] == "ZONE_DWELL":
            dwell_times.append(event["dwell_ms"])

        if event["event_type"] == "ZONE_ENTER":
            zone_counter[event["zone_id"]] += 1

    avg_dwell = (
        sum(dwell_times) / len(dwell_times)
        if dwell_times
        else 0
    )

    return {
        "unique_visitors": len(visitors),
        "total_events": len(events),
        "avg_dwell_ms": round(avg_dwell, 2),
        "most_visited_zone":
            zone_counter.most_common(1)[0][0]
            if zone_counter else None,
        "zone_counts": dict(zone_counter)
    }