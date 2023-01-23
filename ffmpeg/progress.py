from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

# Reference: https://github.com/FFmpeg/FFmpeg/blob/release/5.1/fftools/ffmpeg.c#L1507

_progress_pattern = re.compile(r"(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)")
_time_pattern = re.compile(r"(-?\d+):(\d+):(\d+)\.(\d+)")

_default = {
    "frame": "0",
    "fps": "0.0",
    "size": "0kB",
    "time": "00:00:00.00",
    "bitrate": "0.0kbits/s",
    "speed": "0.0x",
}


def _parse_time(time: str) -> timedelta:
    match = _time_pattern.search(time)
    assert match is not None

    return timedelta(
        hours=int(match.group(1)),
        minutes=int(match.group(2)),
        seconds=int(match.group(3)),
        milliseconds=int(match.group(4)) * 10,
    )


@dataclass(frozen=True)
class Progress:
    """Represents a progress of `FFmpeg` operation.

    Attributes:
        frame: The number of processed frames.
        fps: The processing speed in frame per seconds.
        size: The current size of the media in bytes.
        time: The current time of the media.
        bitrate: The processing speed in kilobits per second.
        speed: The processing speed
    """

    frame: int
    fps: float
    size: int
    time: timedelta
    bitrate: float
    speed: float

    @classmethod
    def from_line(cls, line: str) -> Optional[Progress]:
        items = {key: value for key, value in _progress_pattern.findall(line) if value != "N/A"}
        if not items:
            return None

        progress = {
            **_default,
            **items,
        }

        return Progress(
            frame=int(progress["frame"]),
            fps=float(progress["fps"]),
            size=int(progress["size"].replace("kB", "")) * 1024,
            time=_parse_time(progress["time"]),
            bitrate=float(progress["bitrate"].replace("kbits/s", "")),
            speed=float(progress["speed"].replace("x", "")),
        )
