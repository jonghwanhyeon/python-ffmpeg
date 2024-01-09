import asyncio
from pathlib import Path

import pytest

from ffmpeg.asyncio import FFmpeg


@pytest.mark.asyncio
async def test_asyncio_timeout(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    ffmpeg = (
        FFmpeg()
        .input(str(source_path))
        .output(
            str(target_path),
            codec="copy",
        )
    )

    with pytest.raises(asyncio.TimeoutError):
        await ffmpeg.execute(timeout=0.1)
