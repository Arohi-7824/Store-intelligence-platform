FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

ZONES = {

    # Left product wall
    "SKINCARE_ZONE": (
        744,
        0,
        1110,
        FRAME_HEIGHT
    ),

    # Center promotional/display area
    "DISPLAY_ZONE": (
        1110,
        0,
        1450,
        FRAME_HEIGHT
    ),

    # Billing counter
    "BILLING_ZONE": (
        1450,
        0,
        FRAME_WIDTH,
        FRAME_HEIGHT
    )
}


def point_in_zone(cx, cy, zone_coords):

    x_min, y_min, x_max, y_max = zone_coords

    return (
        x_min <= cx <= x_max
        and y_min <= cy <= y_max
    )


def get_zone(cx, cy):

    for zone_name, zone_coords in ZONES.items():

        if point_in_zone(cx, cy, zone_coords):
            return zone_name

    return "UNKNOWN"