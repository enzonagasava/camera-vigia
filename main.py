import cv2
import threading
import uvicorn
from datetime import datetime
from app.streaming.hls import HLSStream
from app.streaming.server import app
from app.camera.capture import CameraCapture

from app.config import (
    IMAGE_DIR,
    VIDEO_DIR,
    WINDOW_NAME,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FRAME_FPS,
    MOTION_ENABLED,
    MOTION_THRESHOLD,
    SAVE_VIDEO,
    SAVE_MOTION_IMAGES,
    create_directories,
)

from app.processing.motion import MotionDetector
from app.processing.objects import ObjectDetector
from app.processing.pipeline import ProcessingPipeline

from app.storage.video import VideoStorage
from app.storage.images import ImageStorage

def add_timestamp(frame):
    timestamp = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    cv2.putText(
        frame,
        timestamp,
        (frame.shape[1] - 270, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return frame

def main():

    create_directories()

    # ---------------------------------------------------------
    # PROCESSAMENTO
    # ---------------------------------------------------------

    motion_detector = MotionDetector(
        threshold=MOTION_THRESHOLD
    )

    object_detector = ObjectDetector()

    pipeline = ProcessingPipeline(
        motion_detector=motion_detector,
        object_detector=object_detector,
    )

    # ---------------------------------------------------------
    # STORAGE
    # ---------------------------------------------------------

    image_storage = ImageStorage(
        IMAGE_DIR
    )

    video_storage = VideoStorage(
        directory=VIDEO_DIR,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
        fps=FRAME_FPS,
    )

    # ---------------------------------------------------------
    # CAMERA
    # ---------------------------------------------------------

    camera = CameraCapture()

    # ---------------------------------------------------------
    # STREAMING
    #
    # Não acessa /dev/video2.
    # Recebe frames do OpenCV.
    # ---------------------------------------------------------

    STREAM_WIDTH = 1280
    STREAM_HEIGHT = 720
    STREAM_FPS = 15

    hls_stream = HLSStream(
        output_dir="storage/hls",
        width=STREAM_WIDTH,
        height=STREAM_HEIGHT,
        fps=STREAM_FPS,
    )

    try:

        # -----------------------------------------------------
        # GRAVAÇÃO
        # -----------------------------------------------------

        if SAVE_VIDEO:

            video_path = video_storage.start()

            print(
                f"Gravando vídeo em: {video_path}"
            )

        # -----------------------------------------------------
        # HLS
        # -----------------------------------------------------

        hls_stream.start()

        # -----------------------------------------------------
        # HTTP
        # -----------------------------------------------------

        threading.Thread(
            target=lambda: uvicorn.run(
                app,
                host="0.0.0.0",
                port=8001,
                log_level="warning",
            ),
            daemon=True,
        ).start()

        print(
            "Servidor HTTP iniciado na porta 8001."
        )

        print(
            "Câmera iniciada."
        )

        print(
            "Pressione ESC para sair."
        )

        # -----------------------------------------------------
        # STREAM CONTROL
        # -----------------------------------------------------

        stream_frame_interval = 1 / STREAM_FPS

        last_stream_time = 0

        # -----------------------------------------------------
        # LOOP
        # -----------------------------------------------------

        while True:

            # ================================================
            # 1. CAPTURA
            # ================================================

            frame = camera.read()

            # ================================================
            # 2. PROCESSAMENTO
            # ================================================

            result = pipeline.process(
                frame
            )

            processed_frame = result.frame
            
            processed_frame = add_timestamp(processed_frame)
            # ================================================
            # 3. MOVIMENTO
            # ================================================

            if (
                MOTION_ENABLED
                and result.motion_detected
            ):

                cv2.putText(
                    processed_frame,
                    "MOVIMENTO DETECTADO",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )

                if SAVE_MOTION_IMAGES:

                    image_storage.save(
                        processed_frame,
                        prefix="motion",
                    )

            # ================================================
            # 4. STREAMING
            #
            # IMPORTANTE:
            # usamos o frame ORIGINAL.
            #
            # Não usamos processed_frame.
            # ================================================

            current_time = cv2.getTickCount() / cv2.getTickFrequency()

            if (
                current_time - last_stream_time
                >= stream_frame_interval
            ):

                stream_frame = cv2.resize(
                    frame,
                    (
                        STREAM_WIDTH,
                        STREAM_HEIGHT,
                    ),
                    interpolation=cv2.INTER_AREA,
                )

                hls_stream.write(
                    stream_frame
                )

                last_stream_time = current_time

            # ================================================
            # 5. GRAVAÇÃO
            # ================================================

            if SAVE_VIDEO:

                video_storage.write(
                    processed_frame
                )

    except KeyboardInterrupt:

        print(
            "\nInterrupção recebida."
        )

    finally:

        print(
            "Encerrando..."
        )

        hls_stream.stop()

        camera.release()

        if SAVE_VIDEO:
            video_storage.stop()

        cv2.destroyAllWindows()

        print(
            "Aplicação encerrada."
        )


if __name__ == "__main__":
    main()
