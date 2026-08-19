from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

HLS_DIR = Path("storage/hls")

HLS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/hls",
    StaticFiles(
        directory=HLS_DIR
    ),
    name="hls",
)


@app.get(
    "/",
    response_class=HTMLResponse,
)
def index():

    return """
    <!DOCTYPE html>

    <html>

    <head>
        <meta charset="UTF-8">
        <title>Camera</title>

        <style>

            html,
            body {
                margin: 0;
                width: 100%;
                height: 100%;
                background: #000;
            }

            video {
                width: 100%;
                height: 100%;
                object-fit: contain;
            }

        </style>

    </head>

    <body>

        <video
            id="video"
            autoplay
            muted
            playsinline
            controls
        ></video>

        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>

        <script>

            const video =
                document.getElementById("video");

            const source =
                "/hls/stream.m3u8";


            if (Hls.isSupported()) {

                const hls = new Hls({
                    lowLatencyMode: true
                });

                hls.loadSource(source);

                hls.attachMedia(video);

            } else if (
                video.canPlayType(
                    "application/vnd.apple.mpegurl"
                )
            ) {

                video.src = source;

            }

        </script>

    </body>

    </html>
    """