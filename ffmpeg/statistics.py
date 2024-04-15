from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional

from typing_extensions import Self

from ffmpeg.utils import parse_time, parse_size

# Reference: https://github.com/FFmpeg/FFmpeg/blob/release/6.1/fftools/ffmpeg.c#L496

_pattern = re.compile(r"(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)")

_field_factory = {
    "frame": int,
    "fps": float,
    "size": parse_size,
    "time": parse_time,
    "bitrate": lambda item: float(item.replace("kbits/s", "")),
    "speed": lambda item: float(item.replace("x", "")),
}


@dataclass(frozen=True)
class Statistics:
    frame: int = 0
    fps: float = 0.0
    size: int = 0
    time: timedelta = field(default_factory=timedelta)
    bitrate: float = 0.0
    speed: float = 0.0

    @classmethod
    def from_line(cls, line: str) -> Optional[Self]:
        statistics = {key: value for key, value in _pattern.findall(line)}
        if len(statistics) < 4:
            # When a media type is audio,FFmpeg reports the below statistics
            # - size, time, bitrate, speed
            # When a media type is video, FFmpeg reports the below statistics
            # - frame, fps, size, time, bitrate, speed
            return None

        fields = {key: _field_factory[key](value) for key, value in statistics.items() if value != "N/A"}
        return cls(**fields)
