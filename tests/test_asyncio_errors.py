import asyncio
from pathlib import Path

import pytest

from ffmpeg import (
    FFmpegAlreadyStarted,
    FFmpegFileExists,
    FFmpegFileNotFound,
    FFmpegInvalidCommand,
    FFmpegUnsupportedEncoder,
)
from ffmpeg.asyncio import FFmpeg


@pytest.mark.asyncio
async def test_asyncio_raises_already_started(
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
        await ffmpeg.execute()


@pytest.mark.asyncio
async def test_asyncio_raises_file_exists(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    (
        await FFmpeg()
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
            await FFmpeg()
            .input(source_path)
            .output(
                target_path,
                codec="copy",
            )
            .execute()
        )


@pytest.mark.asyncio
async def test_asyncio_raises_file_not_found(
    assets_path: Path,
    tmp_path: Path,
):
    invalid_source_path = assets_path / "non-existent.mp4"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegFileNotFound):
        (
            await FFmpeg()
            .input(invalid_source_path)
            .output(
                target_path,
                codec="copy",
            )
            .execute()
        )


@pytest.mark.asyncio
async def test_asyncio_raises_invalid_command_for_invalid_option(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegInvalidCommand):
        (
            await FFmpeg()
            .option("invalid")
            .input(source_path)
            .output(
                target_path,
                codec="copy",
            )
            .execute()
        )


@pytest.mark.asyncio
async def test_asyncio_raises_invalid_command_for_invalid_file_option(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegInvalidCommand):
        (
            await FFmpeg()
            .option("y")
            .input(
                source_path,
                pix_fmt="yuv420p",
                preset="fast",
            )
            .output(target_path)
            .execute()
        )


@pytest.mark.asyncio
async def test_asyncio_raises_unsupported_encoder(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    with pytest.raises(FFmpegUnsupportedEncoder):
        (
            await FFmpeg()
            .input(source_path)
            .output(
                target_path,
                codec="invalid",
            )
            .execute()
        )
