from __future__ import annotations

from ffmpeg import FFmpeg, Progress


def main():
    ffmpeg = FFmpeg().cmdline("-i input.mp4 -c:v hevc -c:a copy output.mkv")

    @ffmpeg.on("start")
    def on_start(arguments: list[str]):
        print("arguments:", arguments)

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    ffmpeg.execute()


if __name__ == "__main__":
    main()
