from pathlib import Path

from helpers import probe

from ffmpeg import FFmpeg

epsilon = 0.25


def test_input_via_stdin(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with open(source_path, "rb") as source_file:
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("pipe:0")
            .output(
                str(target_path),
                codec="copy",
            )
        )
        ffmpeg.execute(source_file)

    source = probe(source_path)
    target = probe(target_path)

    assert abs(float(source["format"]["duration"]) - float(target["format"]["duration"])) <= epsilon
    assert "mp4" in target["format"]["format_name"]

    assert source["streams"][0]["codec_name"] == target["streams"][0]["codec_name"]
    assert source["streams"][1]["codec_name"] == target["streams"][1]["codec_name"]


def test_output_via_stdout(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "brewing.wav"
    target_path = tmp_path / "brewing.ogg"

    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(source_path)
        .output(
            "pipe:1",
            f="ogg",
        )
    )
    target_bytes = ffmpeg.execute()
    with open(target_path, "wb") as target_file:
        target_file.write(target_bytes)

    source = probe(source_path)
    target = probe(target_path)

    assert abs(float(source["format"]["duration"]) - float(target["format"]["duration"])) <= epsilon
    assert target["format"]["format_name"] == "ogg"
