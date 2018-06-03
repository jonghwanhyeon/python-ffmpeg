import asyncio

from collections import namedtuple
from pyee import EventEmitter

from .utils import build_options, readline, parse_progress


class FFmpegError(Exception):
    pass


class FFmpeg(EventEmitter):
    File = namedtuple('File', ['url', 'options'])

    def __init__(self, executable='ffmpeg'):
        super().__init__()

        self.executable = executable
        self.global_options = {}
        self.input_files = []
        self.output_files = []

        self.executed = False
        self.terminated = False
        self.process = None

        self.on('stderr', self._on_stderr)

    def option(self, key, value=None):
        self.global_options[key] = value
        return self

    def input(self, url, options=None, **kwargs):
        if options is None:
            options = {}

        self.input_files.append(FFmpeg.File(url=url, options={**options, **kwargs}))
        return self

    def output(self, url, options=None, **kwargs):
        if options is None:
            options = {}

        self.output_files.append(FFmpeg.File(url=url, options={**options, **kwargs}))
        return self

    async def execute(self):
        if self.executed:
            raise FFmpegError('FFmpeg is already executed')

        arguments = self._build()
        self.emit('start', arguments)

        self.process = await asyncio.create_subprocess_exec(
            *arguments,
            stderr=asyncio.subprocess.PIPE
        )

        self.executed = True
        await self._read_stderr()
        await self.process.wait()

        if self.process.returncode == 0:
            self.emit('completed')
        elif self.terminated:
            self.emit('terminated')
        else:
            self.emit('error', self.process.returncode)

    def terminate(self):
        if not self.executed:
            raise FFmpegError('FFmpeg is not executed')

        self.terminated = True
        self.process.terminate()

    async def _read_stderr(self):
        async for line in readline(self.process.stderr):
            self.emit('stderr', line.decode('utf-8'))

    def _on_stderr(self, line): # registered in __init__()
        progress = parse_progress(line)
        if progress:
            self.emit('progress', progress)

    def _build(self):
        arguments = [self.executable]
        arguments.extend(build_options(self.global_options))

        for file in self.input_files:
            arguments.extend(build_options(file.options))
            arguments.extend(['-i', file.url])

        for file in self.output_files:
            arguments.extend(build_options(file.options))
            arguments.append(file.url)

        return arguments
