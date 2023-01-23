from __future__ import annotations

import subprocess

from ffmpeg import FFmpeg, Progress


def main():
    streamlink = subprocess.Popen(
        ["streamlink", "--stdout", "https://twitch.tv/zilioner", "best"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    ffmpeg = FFmpeg().option("y").input("pipe:0").output("output.mp4", c="copy")

    @ffmpeg.on("start")
    def on_start(arguments: list[str]):
        print("arguments:", arguments)

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    ffmpeg.execute(streamlink.stdout)


if __name__ == "__main__":
    main()
