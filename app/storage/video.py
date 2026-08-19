from pathlib import Path
from datetime import datetime

import cv2


class VideoStorage:
    def __init__(
        self,
        directory: Path,
        width: int,
        height: int,
        fps: int,
    ):
        self.directory = directory
        self.width = width
        self.height = height
        self.fps = fps

        self.writer = None

    def start(self) -> Path:
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        print (self.fps)
        path = self.directory / f"capture_{timestamp}.mp4"

        codec = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        self.writer = cv2.VideoWriter(
            str(path),
            codec,
            self.fps,
            (self.width, self.height),
        )

        if not self.writer.isOpened():
            raise RuntimeError(
                "Não foi possível iniciar a gravação."
            )

        return path

    def write(self, frame):
        if self.writer is None:
            raise RuntimeError(
                "A gravação ainda não foi iniciada."
            )

        self.writer.write(frame)

    def stop(self):
        if self.writer:
            self.writer.release()
            self.writer = None
