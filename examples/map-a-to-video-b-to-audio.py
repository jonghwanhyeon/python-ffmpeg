from __future__ import annotations

from ffmpeg import FFmpeg, Progress


def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("input-a.mp4")
        .input("input-b.mp4")
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

    ffmpeg.execute()


if __name__ == "__main__":
    main()
