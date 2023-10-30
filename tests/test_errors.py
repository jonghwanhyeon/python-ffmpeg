from pathlib import Path
import ffmpeg
from threading import Thread
import pytest


def test_rerun_raises_FFmpegAlreadyStarted(
    assets_path: Path,
    tmp_path: Path,
):
    input = assets_path / "pier-39.ts"
    output = tmp_path / "pier-39.mp4"
    cmd = (
        ffmpeg.FFmpeg()
        .option("y")
        .input(input)
        .output(output, codec="copy")
    )

    with pytest.raises(ffmpeg.FFmpegAlreadyStarted):
        cmd._executed = True
        cmd.execute()


def test_overwrite_file_raises_FFmpegFileExists(
    assets_path: Path,
    tmp_path: Path,
):
    input = assets_path / "pier-39.ts"
    output = tmp_path / "pier-39.mp4"
    cmd = (
        ffmpeg.FFmpeg()
        .option("y")
        .input(input)
        .output(output, codec="copy")
        .execute()
    )

    with pytest.raises(ffmpeg.FFmpegFileExists):
        (
            ffmpeg.FFmpeg()
            .input(input)
            .output(output, codec="copy")
            .execute()
        )


def test_missing_file_raises_FFmpegFileNotFound(
    assets_path: Path,
    tmp_path: Path,
):
    invalid_input = assets_path / "non-existant.mp4"
    output = tmp_path / "pier-39.mp4"

    with pytest.raises(ffmpeg.FFmpegFileNotFound):
        (
            ffmpeg.FFmpeg()
            .input(invalid_input)
            .output(output, codec="copy")
            .execute()
        )


def test_invalid_command_raises_FFmpegInvalidCommand(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"
    with pytest.raises(ffmpeg.FFmpegInvalidCommand):
        (
            ffmpeg.FFmpeg()
            .option("invalid")
            .input(source_path)
            .output(target_path, codec="copy")
            .execute()
        )


def test_invalid_encoder_option_raises_FFmpegInvalidOption(
    assets_path: Path,
    tmp_path: Path,
):
    input = assets_path / "pier-39.ts"
    output = tmp_path / "output.mp4"

    with pytest.raises(ffmpeg.FFmpegInvalidCommand):
        (
            ffmpeg.FFmpeg()
            .input(input)
            .output(output)
            .option("pix_fmt", "yuv420p")
            .option("preset", "fast")
            .option("y")
            .execute()
        )


def test_unsupported_encoder_raises_FFmpegUnsupportedEncoder(
    assets_path: Path,
    tmp_path: Path,
):
    input = assets_path / "pier-39.ts"
    output = tmp_path / "pier-39.mp4"

    with pytest.raises(ffmpeg.FFmpegUnsupportedEncoder):
        (
            ffmpeg.FFmpeg()
            .input(input)
            .output(output, codec="invalid")
            .execute()
        )
