import collections
import re

Progress = collections.namedtuple('Progress', [
    'frame', 'fps', 'size', 'time', 'bitrate', 'speed'
])

progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

def build_options(options):
    arguments = []

    for key, value in options.items():
        if key.startswith('-'):
            key = key[1:]

        argument = ['-{key}'.format(key=key)]
        if value is not None:
            argument.append(str(value))

        arguments.extend(argument)

    return arguments


async def readlines(stream):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)

        for line in lines:
            yield line

        data.extend(await stream.read(1024))


# Reference: https://github.com/FFmpeg/FFmpeg/blob/master/fftools/ffmpeg.c#L1646
def parse_progress(line):
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
