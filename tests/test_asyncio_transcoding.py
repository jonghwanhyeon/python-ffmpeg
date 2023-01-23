from pathlib import Path

import pytest
from helpers import probe

from ffmpeg.asyncio import FFmpeg

epsilon = 0.25


@pytest.mark.asyncio
async def test_asyncio_transcoding(
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
    await ffmpeg.execute()

    source = probe(source_path)
    target = probe(target_path)

    assert abs(float(source["format"]["duration"]) - float(target["format"]["duration"])) <= epsilon
    assert "mp4" in target["format"]["format_name"]

    assert source["streams"][0]["codec_name"] == target["streams"][0]["codec_name"]
    assert source["streams"][1]["codec_name"] == target["streams"][1]["codec_name"]
