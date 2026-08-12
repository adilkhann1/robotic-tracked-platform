"""
Obstacle candidate detection for a Raspberry Pi tracked robotic platform.

The script captures video from a camera, detects potential obstacles
using OpenCV, draws bounding boxes, and displays basic telemetry.

Controls:
    Q / Esc - exit
    S       - save current frame
"""

import argparse
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_MIN_AREA = 1200


def parse_args():
    """Read command-line parameters."""
    parser = argparse.ArgumentParser(
        description="OpenCV obstacle detection for Raspberry Pi"
    )

    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera index"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH
    )

    parser.add_argument(
        "--height",
        type=int,
        default=DEFAULT_HEIGHT
    )

    parser.add_argument(
        "--min-area",
        type=int,
        default=DEFAULT_MIN_AREA,
        help="Minimum contour area for obstacle detection"
    )

    parser.add_argument(
        "--mode",
        choices=("edges", "hsv"),
        default="edges",
        help="Detection mode"
    )

    parser.add_argument(
        "--show-mask",
        action="store_true",
        help="Display detection mask"
    )

    return parser.parse_args()


def initialize_camera(index, width, height):
    """Initialize and configure camera."""

    camera = cv2.VideoCapture(index)

    if not camera.isOpened():
        raise RuntimeError(
            f"Cannot open camera with index {index}"
        )

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        width
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        height
    )

    return camera


def create_detection_mask(frame, mode):
    """
    Prepare image for obstacle detection.

    Two modes are available:
    - edges: edge-based detection
    - hsv: HSV color segmentation
    """

    if mode == "hsv":

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        # Initial thresholds based on the original prototype.
        # These values can be tuned for different environments.
        lower = np.array(
            [50, 50, 50],
            dtype=np.uint8
        )

        upper = np.array(
            [179, 255, 255],
            dtype=np.uint8
        )

        mask = cv2.inRange(
            hsv,
            lower,
            upper
        )

    else:

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        blurred = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        mask = cv2.Canny(
            blurred,
            50,
            150
        )

    # Remove small gaps and noise
    kernel = np.ones(
        (5, 5),
        dtype=np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    mask = cv2.dilate(
        mask,
        kernel,
        iterations=1
    )

    return mask


def detect_obstacles(mask, min_area, frame_shape):
    """Find potential obstacles in the processed frame."""

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    frame_height, frame_width = frame_shape[:2]
    frame_area = frame_height * frame_width

    obstacles = []

    for contour in contours:

        area = cv2.contourArea(contour)

        # Ignore small objects / noise
        if area < min_area:
            continue

        # Ignore contour covering almost whole image
        if area > frame_area * 0.90:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        center_x = x + w // 2
        center_y = y + h // 2

        obstacles.append(
            {
                "area": area,
                "bbox": (x, y, w, h),
                "center": (center_x, center_y)
            }
        )

    # Largest detected objects first
    obstacles.sort(
        key=lambda item: item["area"],
        reverse=True
    )

    return obstacles


def draw_obstacles(frame, obstacles):
    """Draw detected obstacles on the camera image."""

    for index, obstacle in enumerate(
        obstacles,
        start=1
    ):

        x, y, w, h = obstacle["bbox"]

        center_x, center_y = obstacle["center"]

        area = obstacle["area"]

        # Bounding box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Object center
        cv2.circle(
            frame,
            (center_x, center_y),
            4,
            (0, 0, 255),
            -1
        )

        label = (
            f"Obstacle {index} "
            f"| area: {int(area)}"
        )

        text_y = max(
            y - 10,
            20
        )

        cv2.putText(
            frame,
            label,
            (x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            2
        )


def draw_status(frame, fps, obstacle_count, mode):
    """Display basic system telemetry."""

    status = (
        f"Mode: {mode} | "
        f"FPS: {fps:.1f} | "
        f"Objects: {obstacle_count}"
    )

    cv2.putText(
        frame,
        status,
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    if obstacle_count > 0:

        cv2.putText(
            frame,
            "OBSTACLE DETECTED",
            (10, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )


def save_frame(frame, directory="captures"):
    """Save current camera frame."""

    output_dir = Path(directory)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    path = (
        output_dir /
        f"capture_{timestamp}.jpg"
    )

    cv2.imwrite(
        str(path),
        frame
    )

    print(
        f"[INFO] Saved frame: {path}"
    )


def main():

    args = parse_args()

    camera = initialize_camera(
        args.camera,
        args.width,
        args.height
    )

    previous_time = time.perf_counter()

    print("[INFO] Camera started")
    print(
        "[INFO] Press Q or Esc to exit, "
        "S to save frame"
    )

    try:

        while True:

            success, frame = camera.read()

            if not success:

                print(
                    "[WARNING] Failed to read "
                    "frame from camera"
                )

                break

            # Image preprocessing
            mask = create_detection_mask(
                frame,
                args.mode
            )

            # Object detection
            obstacles = detect_obstacles(
                mask,
                args.min_area,
                frame.shape
            )

            # Visualization
            draw_obstacles(
                frame,
                obstacles
            )

            # Calculate FPS
            current_time = time.perf_counter()

            elapsed = (
                current_time -
                previous_time
            )

            fps = (
                1.0 / elapsed
                if elapsed > 0
                else 0.0
            )

            previous_time = current_time

            draw_status(
                frame,
                fps,
                len(obstacles),
                args.mode
            )

            cv2.imshow(
                "Robotic Tracked Platform - Camera",
                frame
            )

            if args.show_mask:

                cv2.imshow(
                    "Detection Mask",
                    mask
                )

            key = cv2.waitKey(1) & 0xFF

            # Esc or Q
            if key in (
                27,
                ord("q")
            ):
                break

            # Save screenshot
            if key == ord("s"):
                save_frame(frame)

    finally:

        camera.release()

        cv2.destroyAllWindows()

        print("[INFO] Camera stopped")


if __name__ == "__main__":
    main()
