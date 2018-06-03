import asyncio
import collections

from pyee import EventEmitter

from .utils import build_options, readline, parse_progress

class FFmpegError(Exception):
    pass

class FFmpeg(EventEmitter):
    File = collections.namedtuple('File', ['url', 'options'])

    def __init__(self, executable='ffmpeg'):
        super().__init__()

        self.executable = executable

        self.global_options = {}
        self.input_files = []
        self.output_files = []

        self.executed = False
        self.process = None

    def global_option(self, key, value=None):
        self.global_options[key] = value
        return self

    def input_file(self, url, **kwargs):
        self.input_files.append(FFmpeg.File(
            url=url,
            options=kwargs
        ))
        return self

    def output_file(self, url, **kwargs):
        self.output_files.append(FFmpeg.File(
            url=url,
            options=kwargs
        ))
        return self

    async def run(self):
        if self.executed:
            raise FFmpegError('FFmpeg is already executed')

        async def read_progress(process):
            async for line in readline(process.stderr):
                progress = parse_progress(line.decode('utf-8'))
                if progress:
                    self.emit('progress', process, progress)

        self.process = await asyncio.create_subprocess_exec(
            *self._build(),
            stderr=asyncio.subprocess.PIPE
        )
        self.executed = True

        await read_progress(self.process)

        await self.process.wait()
        self.emit('completed', self.process)

    def _build(self):
        arguments = [self.executable]
        arguments += build_options(self.global_options)

        for file in self.input_files:
            arguments += build_options(file.options)
            arguments += ['-i', file.url]

        for file in self.output_files:
            arguments += build_options(file.options)
            arguments += [file.url]

        return arguments
