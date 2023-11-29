from pathlib import Path

import pytest

from ffmpeg import (
    FFmpeg,
    FFmpegAlreadyExecuted,
    FFmpegFileExists,
    FFmpegFileNotFound,
    FFmpegInvalidCommand,
    FFmpegUnsupportedCodec,
)


def test_raises_already_executed(
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

    with pytest.raises(FFmpegAlreadyExecuted):
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
        # Note: pytest sets stdin to a null object, so "Overwrite? [y/N]" prompt will be ignored
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
            .input(
                source_path,
                pix_fmt="yuv420p",
                preset="fast",
            )
            .output(target_path)
            .execute()
        )


def test_raises_unsupported_codec_for_invalid_decoder(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegUnsupportedCodec):
        (
            FFmpeg()
            .input(
                source_path,
                codec="invalid",
            )
            .output(
                target_path,
            )
            .execute()
        )


def test_raises_unsupported_codec_for_invalid_encoders(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegUnsupportedCodec):
        (
            FFmpeg()
            .input(source_path)
            .output(
                target_path,
                codec="invalid",
            )
            .execute()
        )
