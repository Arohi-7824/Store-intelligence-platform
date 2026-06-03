from zone_tracker import process_zone_change

print(process_zone_change(1, "LEFT_ZONE"))

for i in range(15):
    events = process_zone_change(1, "CENTER_ZONE")

    if events:
        print(events)