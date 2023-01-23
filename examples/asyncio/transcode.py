from __future__ import annotations

import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg


async def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("input.mp4")
        .output(
            "ouptut.mp4",
            {"codec:v": "libx264", "filter:v": "scale=1280:-1"},
            preset="veryslow",
            crf=24,
        )
    )

    @ffmpeg.on("start")
    def on_start(arguments: list[str]):
        print("arguments:", arguments)

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    await ffmpeg.execute()


if __name__ == "__main__":
    asyncio.run(main())
