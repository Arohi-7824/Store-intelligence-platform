import json
import cv2
import numpy as np


def generate_heatmap(
    tracks_file,
    output_file="heatmap.png"
):

    points = []

    max_x = 0
    max_y = 0

    # Read all track points
    with open(tracks_file, "r") as f:

        for line in f:

            point = json.loads(line)

            x = int(point["cx"])
            y = int(point["cy"])

            points.append((x, y))

            max_x = max(max_x, x)
            max_y = max(max_y, y)

    print(f"Loaded {len(points)} points")
    print(f"Canvas Size: {max_x + 50} x {max_y + 50}")

    width = max_x + 50
    height = max_y + 50

    heatmap = np.zeros(
        (height, width),
        dtype=np.float32
    )

    # Draw density circles
    for x, y in points:

        cv2.circle(
            heatmap,
            (x, y),
            30,
            25,
            -1
        )

    # Smooth hotspots
    heatmap = cv2.GaussianBlur(
        heatmap,
        (0, 0),
        sigmaX=60,
        sigmaY=60
    )

    # Log scaling helps reveal medium-density areas
    heatmap = np.log1p(heatmap)

    # Normalize to image range
    heatmap = cv2.normalize(
        heatmap,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    heatmap = heatmap.astype(np.uint8)

    # Apply color map
    heatmap_color = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    # Optional dark background
    background = np.zeros(
        (height, width, 3),
        dtype=np.uint8
    )

    overlay = cv2.addWeighted(
        background,
        0.2,
        heatmap_color,
        0.8,
        0
    )

    cv2.imwrite(
        output_file,
        overlay
    )

    print(f"Heatmap saved to: {output_file}")

    return output_file