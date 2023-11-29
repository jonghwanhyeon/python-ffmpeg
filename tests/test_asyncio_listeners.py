from pathlib import Path

import pytest

from ffmpeg.asyncio import FFmpeg


@pytest.mark.asyncio
async def test_asyncio_exception_raising(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    raised_error = RuntimeError("Raised error")
    caught_error = None

    ffmpeg = (
        FFmpeg()
        .input(str(source_path))
        .output(
            str(target_path),
            codec="copy",
        )
    )

    @ffmpeg.on("start")
    def raise_error_on_start(args):
        raise raised_error

    try:
        await ffmpeg.execute()
    except Exception as exc:
        caught_error = exc

    assert caught_error == raised_error
