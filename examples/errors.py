from __future__ import annotations

from ffmpeg import FFmpeg, FFmpegFileNotFound, FFmpegInvalidCommand


def main():
    try:
        ffmpeg = FFmpeg().input("non-existent.mp4").output("output.mp4")
        ffmpeg.execute()
    except FFmpegFileNotFound as exception:
        print("An exception has been occurred!")
        print("- Message from ffmpeg:", exception.message)
        print("- Arguments to execute ffmpeg:", exception.arguments)

    try:
        ffmpeg = FFmpeg().input("input.mp4", invalid="option").output("output.mp4")
        ffmpeg.execute()
    except FFmpegInvalidCommand as exception:
        print("An exception has been occurred!")
        print("- Message from ffmpeg:", exception.message)
        print("- Arguments to execute ffmpeg:", exception.arguments)


if __name__ == "__main__":
    main()
