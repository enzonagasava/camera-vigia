from app.processing.motion import MotionDetector
from app.processing.objects import ObjectDetector


class ProcessingResult:

    def __init__(
        self,
        frame,
        motion_detected: bool = False,
        movement_pixels: int = 0,
        objects: list | None = None,
    ):
        self.frame = frame
        self.motion_detected = motion_detected
        self.movement_pixels = movement_pixels
        self.objects = objects or []


class ProcessingPipeline:

    def __init__(
        self,
        motion_detector: MotionDetector | None = None,
        object_detector: ObjectDetector | None = None,
    ):
        self.motion_detector = motion_detector
        self.object_detector = object_detector

    def process(self, frame) -> ProcessingResult:

        motion_detected = False
        movement_pixels = 0
        objects = []

        if self.motion_detector is not None:

            (
                motion_detected,
                movement_pixels,
                _,
            ) = self.motion_detector.detect(frame)

        if self.object_detector is not None:

            objects = self.object_detector.detect(frame)

        return ProcessingResult(
            frame=frame,
            motion_detected=motion_detected,
            movement_pixels=movement_pixels,
            objects=objects,
        )
