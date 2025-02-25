import asyncio
from pathlib import Path

import pytest
from helpers import probe

from ffmpeg.asyncio import FFmpeg

epsilon = 0.25


async def yield_async_chunks(source_path: Path, sleep: float = 0.001, sleep_every: int = 1000):
    with open(source_path, "rb") as source_file:
        for i, source_bytes_chunk in enumerate(source_file):
            yield source_bytes_chunk
            if i % sleep_every == 0:
                await asyncio.sleep(sleep)


@pytest.mark.asyncio
async def test_async_iterable_input_via_stdin(
    assets_path: Path,
    tmp_path: Path,
):
    source_path = assets_path / "pier-39.ts"
    target_path = tmp_path / "pier-39.mp4"

    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("pipe:0")
        .output(
            str(target_path),
            codec="copy",
        )
    )

    await ffmpeg.execute(yield_async_chunks(source_path))

    source = probe(source_path)
    target = probe(target_path)

    assert abs(float(source["format"]["duration"]) - float(target["format"]["duration"])) <= epsilon
    assert "mp4" in target["format"]["format_name"]

    assert source["streams"][0]["codec_name"] == target["streams"][0]["codec_name"]
    assert source["streams"][1]["codec_name"] == target["streams"][1]["codec_name"]
