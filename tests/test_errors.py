from pathlib import Path

import pytest

from ffmpeg import (
    FFmpeg,
    FFmpegAlreadyStarted,
    FFmpegFileExists,
    FFmpegFileNotFound,
    FFmpegInvalidCommand,
    FFmpegUnsupportedEncoder,
)


def test_raises_already_started(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(source_path)
        .output(
            target_path,
            codec="copy",
        )
    )

    with pytest.raises(FFmpegAlreadyStarted):
        ffmpeg._executed = True
        ffmpeg.execute()


def test_raises_file_exists(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    (
        FFmpeg()
        .option("y")
        .input(source_path)
        .output(
            target_path,
            codec="copy",
        )
        .execute()
    )

    with pytest.raises(FFmpegFileExists):
        (
            FFmpeg()
            .input(source_path)
            .output(
                target_path,
                codec="copy",
            )
            .execute()
        )


def test_raises_file_not_found(
    assets_path: Path,
    tmp_path: Path,
):
    invalid_source_path = assets_path / "non-existent.mp4"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegFileNotFound):
        (
            FFmpeg()
            .input(invalid_source_path)
            .output(
                target_path,
                codec="copy",
            )
            .execute()
        )


def test_raises_invalid_command_for_invalid_option(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegInvalidCommand):
        (
            FFmpeg()
            .option("invalid")
            .input(source_path)
            .output(
                target_path,
                codec="copy",
            )
            .execute()
        )


def test_raises_invalid_command_for_invalid_file_option(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegInvalidCommand):
        (
            FFmpeg()
            .option("y")
            .input(source_path)
            .output(target_path)
            .option("pix_fmt", "yuv420p")
            .option("preset", "fast")
            .execute()
        )


def test_raises_unsupported_encoder(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegUnsupportedEncoder):
        (
            FFmpeg()
            .input(source_path)
            .output(
                target_path,
                codec="invalid",
            )
            .execute()
        )
