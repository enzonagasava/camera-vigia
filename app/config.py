from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

STORAGE_DIR = BASE_DIR / "storage"
VIDEO_DIR = STORAGE_DIR / "videos"
IMAGE_DIR = STORAGE_DIR / "images"

CAMERA_DEVICE = 3

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_FPS = 12

WINDOW_NAME = "Camera App"

MOTION_ENABLED = True
MOTION_THRESHOLD = 5000

SAVE_VIDEO = True
SAVE_MOTION_IMAGES = True


def create_directories() -> None:
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
