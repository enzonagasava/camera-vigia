from app.camera.device import CameraDevice
from app.config import (
    CAMERA_DEVICE,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FRAME_FPS,
)


class CameraCapture:
    def __init__(self):
        self.device = CameraDevice(
            device=CAMERA_DEVICE,
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            fps=FRAME_FPS,
        )

    def read(self):
        return self.device.read()

    def release(self):
        self.device.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
