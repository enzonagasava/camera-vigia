import subprocess
from pathlib import Path
import threading


class HLSStream:

    def __init__(
        self,
        output_dir: str,
        width: int = 1920,
        height: int = 1080,
        fps: int = 15,
    ):
        self.output_dir = Path(output_dir)

        self.width = width
        self.height = height
        self.fps = fps

        self.process = None
        self._lock = threading.Lock()

    def start(self):

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = self.output_dir / "stream.m3u8"

        command = [
            "ffmpeg",

            "-hide_banner",
            "-loglevel",
            "warning",

            # Receber frames pelo stdin
            "-f",
            "rawvideo",

            "-pix_fmt",
            "bgr24",

            "-video_size",
            f"{self.width}x{self.height}",

            "-framerate",
            str(self.fps),

            "-i",
            "-",
            
            "-vf",
            "drawtext="
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:"
            "text='%{localtime}':"
            "x=w-tw-20:"
            "y=20:"
            "fontsize=28:"
            "fontcolor=white:"
            "box=1:"
            "boxcolor=black@0.6:"
            "boxborderw=10", 
                        
            # H264
            "-c:v",
            "libx264",

            "-preset",
            "veryfast",
            
            "-g", "15",
            "-keyint_min", "1",
            "-sc_threshold", "0",

            "-force_key_frames", "expr:gte(t,n_forced*1)",


            "-tune",
            "zerolatency",

            "-pix_fmt",
            "yuv420p",

            "-crf",
            "28",

            # HLS
            "-f",
            "hls",

            "-hls_time",
            "1",

            "-hls_list_size",
            "3",

            "-hls_flags",
            "delete_segments+omit_endlist",

            str(output),
        ]

        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
        )

        print(
            f"Streaming HLS iniciado: {output}"
        )

    def write(self, frame):

        if self.process is None:
            return

        if self.process.stdin is None:
            return

        try:

            with self._lock:

                self.process.stdin.write(
                    frame.tobytes()
                )

                self.process.stdin.flush()

        except (
            BrokenPipeError,
            ValueError,
        ):

            self.stop()

    def stop(self):

        if self.process is None:
            return

        try:

            if self.process.stdin:
                self.process.stdin.close()

            self.process.wait(
                timeout=3
            )

        except (
            subprocess.TimeoutExpired,
            BrokenPipeError,
            ValueError,
        ):

            self.process.kill()

        finally:

            self.process = None
