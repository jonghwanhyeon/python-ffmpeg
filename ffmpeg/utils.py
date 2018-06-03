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


async def readline(stream):
    pattern = re.compile(br'\r\n|\r|\n')

    data = bytearray()
    while not stream.at_eof():
        data.extend(await stream.read(1))

        lines = pattern.split(data)
        for line in lines[:-1]:
            yield line

        data[:] = lines[-1]


def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }

    if not items:
        return None

    return Progress(
        frame=int(items['frame']),
        fps=int(items['frame']),
        size=int(items['size'].replace('kB', '')) * 1024,
        time=items['time'],
        bitrate=float(items['bitrate'].replace('kbits/s', '')),
        speed=float(items['speed'].replace('x', '')),
    )
