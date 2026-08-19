import cv2


class MotionDetector:
    def __init__(self, threshold: int = 5000):
        self.threshold = threshold
        self.previous_frame = None

    def detect(self, frame) -> tuple[bool, int, object]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(
            gray,
            (21, 21),
            0,
        )

        if self.previous_frame is None:
            self.previous_frame = gray
            return False, 0, frame

        difference = cv2.absdiff(
            self.previous_frame,
            gray,
        )

        _, threshold = cv2.threshold(
            difference,
            25,
            255,
            cv2.THRESH_BINARY,
        )

        threshold = cv2.dilate(
            threshold,
            None,
            iterations=2,
        )

        movement_pixels = cv2.countNonZero(threshold)

        motion_detected = movement_pixels > self.threshold

        self.previous_frame = gray

        return (
            motion_detected,
            movement_pixels,
            threshold,
        )
