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


def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }

    if not items:
        return None

    if items['size'] == 'N/A':
        size = None
    else:
        size = int(items['size'].replace('kB', '')) * 1024

    if items['bitrate'] == 'N/A':
        bitrate = None
    else:
        bitrate = float(items['size'].replace('kbits/s', ''))

    return Progress(
        frame=int(items['frame']),
        fps=float(items['fps']),
        size=size,
        time=items['time'],
        bitrate=bitrate,
        speed=float(items['speed'].replace('x', '')),
    )
