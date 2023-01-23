from __future__ import annotations

import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg


async def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(
            "rtsp://username@password:127.0.0.1/cam",
            rtsp_transport="tcp",
            rtsp_flags="prefer_tcp",
        )
        .output("output.mp4", vcodec="copy")
    )

    @ffmpeg.on("start")
    def on_start(arguments: list[str]):
        print("arguments:", arguments)

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    @ffmpeg.on("progress")
    def time_to_terminate(progress: Progress):
        if progress.frame > 200:
            ffmpeg.terminate()

    await ffmpeg.execute()


if __name__ == "__main__":
    asyncio.run(main())
