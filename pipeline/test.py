from events import create_zone_enter_event

event = create_zone_enter_event(
    visitor_id="VIS_1",
    zone_id="LEFT_ZONE"
)

print(event)