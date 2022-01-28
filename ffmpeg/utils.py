import asyncio
import collections
import re
from typing import Dict, List

from .typing import Option

Progress = collections.namedtuple('Progress', [
    'frame', 'fps', 'size', 'time', 'bitrate', 'speed'
])

progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

def build_option(key: str, value: Option) -> List[str]:
    if key.startswith('-'):
        key = key[1:]

    option = [f'-{key}']
    if value is not None:
        option.append(str(value))

    return option

def build_options(options: Dict[str, Option]) -> List[str]:
    arguments = []

    for key, values in options.items():
        if not isinstance(values, (list, set, tuple)):
            values = [values]

        for value in values:
            arguments.extend(build_option(key, value))

    return arguments


async def readlines(stream: asyncio.StreamReader):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)

        for line in lines:
            yield line

        data.extend(await stream.read(1024))


# Reference: https://github.com/FFmpeg/FFmpeg/blob/master/fftools/ffmpeg.c#L1646
def parse_progress(line: str) -> Progress:
    default = {
        'frame': '0',
        'fps': '0.0',
        'size': '0kB',
        'time': '00:00:00.00',
        'bitrate': '0.0kbits/s',
        'speed': '0.0x',
    }

    items = {
        key: value for key, value in progress_pattern.findall(line) if value != 'N/A'
    }

    if not items:
        return None

    progress = {
        **default,
        **items,
    }

    return Progress(
        frame=int(progress['frame']),
        fps=float(progress['fps']),
        size=int(progress['size'].replace('kB', '')) * 1024,
        time=progress['time'],
        bitrate=float(progress['bitrate'].replace('kbits/s', '')),
        speed=float(progress['speed'].replace('x', '')),
    )
