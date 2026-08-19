from pathlib import Path
from datetime import datetime

import cv2


class ImageStorage:
    def __init__(self, directory: Path):
        self.directory = directory

    def save(self, frame, prefix: str = "capture") -> Path:
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        path = self.directory / (
            f"{prefix}_{timestamp}.jpg"
        )

        success = cv2.imwrite(
            str(path),
            frame,
        )

        if not success:
            raise RuntimeError(
                f"Não foi possível salvar a imagem: {path}"
            )

        return path
