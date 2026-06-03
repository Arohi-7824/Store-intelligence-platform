import json

def clear_events_file():
    open("data/events/events.jsonl", "w").close()

def write_event(event):

    with open(
        "data/events/events.jsonl",
        "a"
    ) as f:

        f.write(
            json.dumps(event)
        )

        f.write("\n")