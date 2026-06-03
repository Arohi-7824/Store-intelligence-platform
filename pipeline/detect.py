from ultralytics import YOLO
import cv2
import json

from zones import ZONES, get_zone
from zone_tracker import process_zone_change
from event_writer import write_event, clear_events_file


# ----------------------------------
# Reset files before processing
# ----------------------------------

clear_events_file()

with open("data/tracks/tracks.jsonl", "w"):
    pass


# ----------------------------------
# Open track file once
# ----------------------------------

track_file = open(
    "data/tracks/tracks.jsonl",
    "a"
)


# ----------------------------------
# Load model and video
# ----------------------------------

VIDEO_PATH = "data/videos/CAM1.mp4"

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO_PATH)


# ----------------------------------
# Main processing loop
# ----------------------------------

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0],          # person only
        conf=0.4,
        iou=0.5,
        verbose=False
    )

    result = results[0]

    if result.boxes.id is not None:

        boxes = result.boxes.xyxy.cpu().numpy()
        ids = result.boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, ids):

            x1, y1, x2, y2 = map(int, box)

            # --------------------------
            # Person center point
            # --------------------------

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # --------------------------
            # Save tracking point
            # --------------------------

            json.dump(
                {
                    "visitor_id": f"VIS_{int(track_id)}",
                    "cx": cx,
                    "cy": cy,
                    "frame": int(
                        cap.get(cv2.CAP_PROP_POS_FRAMES)
                    )
                },
                track_file
            )

            track_file.write("\n")

            # --------------------------
            # Zone Detection
            # --------------------------

            zone = get_zone(cx, cy)

            # --------------------------
            # Zone Event Generation
            # --------------------------

            events = process_zone_change(
                int(track_id),
                zone
            )

            for event in events:

                print(event)

                write_event(event)

    # ----------------------------------
    # Visualization
    # ----------------------------------

    annotated = result.plot()

    for zone_name, coords in ZONES.items():

        x1, y1, x2, y2 = coords

        cv2.rectangle(
            annotated,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            3
        )

        cv2.putText(
            annotated,
            zone_name,
            (x1 + 10, y1 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Tracking",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ----------------------------------
# Cleanup
# ----------------------------------

track_file.close()

cap.release()

cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()