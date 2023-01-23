from __future__ import annotations

import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg


async def main():
    streamlink = await asyncio.create_subprocess_exec(
        "streamlink",
        "--stdout",
        "https://twitch.tv/zilioner",
        "best",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )

    ffmpeg = FFmpeg().option("y").input("pipe:0").output("output.mp4", c="copy")

    @ffmpeg.on("start")
    def on_start(arguments: list[str]):
        print("arguments:", arguments)

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    await ffmpeg.execute(streamlink.stdout)


if __name__ == "__main__":
    asyncio.run(main())
