import asyncio

from collections import namedtuple
from pyee import EventEmitter

from .utils import build_options, readline, parse_progress


class FFmpegError(Exception):
    pass


class FFmpeg(EventEmitter):
    _File = namedtuple('_File', ['url', 'options'])

    def __init__(self, executable='ffmpeg'):
        super().__init__()

        self._executable = executable
        self._global_options = {}
        self._input_files = []
        self._output_files = []

        self._executed = False
        self._terminated = False
        self._process = None

        self.on('stderr', self._on_stderr)

    def option(self, key, value=None):
        self._global_options[key] = value
        return self

    def input(self, url, options=None, **kwargs):
        if options is None:
            options = {}

        self._input_files.append(FFmpeg._File(url=url, options={**options, **kwargs}))
        return self

    def output(self, url, options=None, **kwargs):
        if options is None:
            options = {}

        self._output_files.append(FFmpeg._File(url=url, options={**options, **kwargs}))
        return self

    @property
    def process(self):
        return self._process

    async def execute(self):
        if self._executed:
            raise FFmpegError('FFmpeg is already executed')

        arguments = self._build()
        self.emit('start', arguments)

        self._process = await asyncio.create_subprocess_exec(
            *arguments,
            stderr=asyncio.subprocess.PIPE
        )

        self._executed = True
        await self._read_stderr()
        await self._process.wait()

        if self._process.returncode == 0:
            self.emit('completed')
        elif self._terminated:
            self.emit('terminated')
        else:
            self.emit('error', self._process.returncode)

    def terminate(self):
        if not self._executed:
            raise FFmpegError('FFmpeg is not executed')

        self._terminated = True
        self._process.terminate()

    async def _read_stderr(self):
        async for line in readline(self._process.stderr):
            self.emit('stderr', line.decode('utf-8'))

    def _on_stderr(self, line): # registered in __init__()
        progress = parse_progress(line)
        if progress:
            self.emit('progress', progress)

    def _build(self):
        arguments = [self._executable]
        arguments.extend(build_options(self._global_options))

        for file in self._input_files:
            arguments.extend(build_options(file.options))
            arguments.extend(['-i', file.url])

        for file in self._output_files:
            arguments.extend(build_options(file.options))
            arguments.append(file.url)

        return arguments
