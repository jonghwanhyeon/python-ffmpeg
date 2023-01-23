import os
from pathlib import Path

from ffmpeg.options import Options


def test_options(assets_path: Path, tmp_path: Path):
    pier39_path = assets_path / "pier-39.mov"
    snow_path = assets_path / "snow.mov"
    output_path = tmp_path / "output.mp4"

    options = Options()
    options.option("y")
    assert [*options.build()] == ["-y"]

    options = Options()
    options.option("y")
    options.option("loglevel", "verbose")
    assert [*options.build()] == ["-y", "-loglevel", "verbose"]

    options = Options()
    options.option("y")
    options.input(pier39_path, codec="copy")
    assert [*options.build()] == ["-y", "-codec", "copy", "-i", os.fspath(pier39_path)]

    options = Options()
    options.option("y")
    options.input(pier39_path)
    options.output(
        output_path,
        {"codec:v": "libx264"},
        preset="veryfast",
        crf=24,
    )
    assert [*options.build()] == [
        # fmt: off
        "-y",
        "-i", os.fspath(pier39_path),
        "-codec:v", "libx264",
        "-preset", "veryfast",
        "-crf", "24",
        os.fspath(output_path),
        # fmt: on
    ]

    options = Options()
    options.option("y")
    options.input(pier39_path)
    options.input(snow_path)
    options.output(output_path, map=["0:v", "1:a"])
    assert [*options.build()] == [
        # fmt: off
        "-y",
        "-i", os.fspath(pier39_path),
        "-i", os.fspath(snow_path),
        "-map", "0:v",
        "-map", "1:a",
        os.fspath(output_path),
        # fmt: on
    ]
