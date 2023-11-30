from __future__ import annotations

import json

from ffmpeg import FFmpeg


def main():
    ffmpeg = FFmpeg(executable="ffprobe").input(
        "input.mp4",
        print_format="json",
        show_streams=None,
    )

    media = json.loads(ffmpeg.execute())

    print(f"# Video")
    print(f"- Codec: {media['streams'][0]['codec_name']}")
    print(f"- Resolution: {media['streams'][0]['width']} X {media['streams'][0]['height']}")
    print(f"- Duration: {media['streams'][0]['duration']}")
    print("")

    print(f"# Audio")
    print(f"- Codec: {media['streams'][1]['codec_name']}")
    print(f"- Sample Rate: {media['streams'][1]['sample_rate']}")
    print(f"- Duration: {media['streams'][1]['duration']}")


if __name__ == "__main__":
    main()
