import time

from dwell_tracker import (
    record_zone_entry,
    process_zone_exit
)

record_zone_entry(
    "VIS_1",
    "CENTER_ZONE"
)

time.sleep(5)

event = process_zone_exit(
    "VIS_1",
    "CENTER_ZONE"
)

print(event)