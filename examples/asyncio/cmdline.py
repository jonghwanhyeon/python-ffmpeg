from __future__ import annotations

import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg


async def main():
    ffmpeg = FFmpeg().cmdline("-i input.mp4 -c:v hevc -c:a copy output.mkv")

    @ffmpeg.on("start")
    def on_start(arguments: list[str]):
        print("arguments:", arguments)

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    await ffmpeg.execute()


if __name__ == "__main__":
    asyncio.run(main())
