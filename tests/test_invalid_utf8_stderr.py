import os
import stat
from pathlib import Path

import pytest

from ffmpeg import FFmpeg
from ffmpeg.asyncio import FFmpeg as AsyncFFmpeg

# Real ffmpeg truncates long metadata values (title/comment/etc.) at a fixed
# byte length when logging them to stderr, without regard for multi-byte
# UTF-8 character boundaries. That can leave an incomplete sequence at the
# cut point which is not valid UTF-8, even though the source text was.
#
# These tests use a stub "ffmpeg" that deterministically reproduces that
# byte sequence, rather than depending on real ffmpeg's undocumented
# truncation behavior (which is awkward to trigger reliably in a test).
_STUB_SCRIPT = """\
#!/usr/bin/env python3
import sys

# An incomplete 3-byte UTF-8 sequence (as if a multi-byte character got cut
# off mid-character by ffmpeg's own truncation), followed by a normal,
# fully valid progress stats line.
sys.stderr.buffer.write(b"    comment         : \\xe3\\x81\\n")
sys.stderr.buffer.write(
    b"frame=  100 fps=25.0 q=1.0 size=100kB time=00:00:01.00 "
    b"bitrate=100.0kbits/s speed=1.0x\\n"
)
sys.stderr.buffer.flush()
sys.stdout.buffer.write(b"ok")
sys.stdout.buffer.flush()
sys.exit(0)
"""


@pytest.fixture
def stub_ffmpeg(tmp_path: Path) -> str:
    script_path = tmp_path / "stub_ffmpeg.py"
    script_path.write_text(_STUB_SCRIPT)
    script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    return str(script_path)


def test_invalid_utf8_stderr_does_not_raise(stub_ffmpeg: str):
    ffmpeg = FFmpeg(executable=stub_ffmpeg)

    stderr_lines = []
    ffmpeg.on("stderr", stderr_lines.append)

    progress_events = []
    ffmpeg.on("progress", progress_events.append)

    # Must not raise UnicodeDecodeError.
    ffmpeg.execute()

    assert len(stderr_lines) == 2
    assert "�" in stderr_lines[0]  # the malformed line was replaced, not dropped
    assert stderr_lines[1].startswith("frame=")

    # The valid line after the malformed one must still be tracked normally.
    assert len(progress_events) == 1
    assert progress_events[0].frame == 100


@pytest.mark.asyncio
async def test_asyncio_invalid_utf8_stderr_does_not_raise(stub_ffmpeg: str):
    ffmpeg = AsyncFFmpeg(executable=stub_ffmpeg)

    stderr_lines = []
    ffmpeg.on("stderr", stderr_lines.append)

    progress_events = []
    ffmpeg.on("progress", progress_events.append)

    # Must not raise UnicodeDecodeError.
    await ffmpeg.execute()

    assert len(stderr_lines) == 2
    assert "�" in stderr_lines[0]
    assert stderr_lines[1].startswith("frame=")

    assert len(progress_events) == 1
    assert progress_events[0].frame == 100
