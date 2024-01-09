import subprocess
from pathlib import Path

import pytest

from ffmpeg import FFmpeg


def test_transcoding(
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

    with pytest.raises(subprocess.TimeoutExpired):
        ffmpeg.execute(timeout=0.1)
