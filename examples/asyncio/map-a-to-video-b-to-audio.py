from __future__ import annotations

import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg


async def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("input-a.ts")
        .input("input-b.ts")
        .output(
            "output.mp4",
            map=["0:0", "1:1"],
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
