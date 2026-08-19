import cv2


class CameraDevice:
    def __init__(
        self,
        device: int = 0,
        width: int = 1280,
        height: int = 720,
        fps: int = 30,
    ):
        self.device = device

        self.capture = cv2.VideoCapture(device, cv2.CAP_V4L2,)

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Não foi possível abrir a câmera {device}."
            )
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"mp4v"),)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.capture.set(cv2.CAP_PROP_FPS, fps)
        self.capture.set(cv2.CAP_PROP_BRIGHTNESS, 0.7,)
        print(
            "FPS:",
            self.capture.get(cv2.CAP_PROP_FPS)
        )
 
    def read(self):
        success, frame = self.capture.read()

        if not success:
            raise RuntimeError(
                "Não foi possível capturar um frame da câmera."
            )

        return frame

    def release(self):
        if self.capture:
            self.capture.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

