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

        self._executable = executable

        self._global_options = {}
        self._input_files = []
        self._output_files = []

    def global_option(self, key, value=None):
        self._global_options[key] = value
        return self

    def input_file(self, url, **kwargs):
        self._input_files.append(FFmpeg.File(
            url=url,
            options=kwargs
        ))
        return self

    def output_file(self, url, **kwargs):
        self._output_files.append(FFmpeg.File(
            url=url,
            options=kwargs
        ))
        return self

    async def run(self):
        async def read_progress(process):
            async for line in readline(process.stderr):
                progress = parse_progress(line.decode('utf-8'))
                if progress:
                    self.emit('progress', process, progress)

        process = await asyncio.create_subprocess_exec(
            *self._build(),
            stderr=asyncio.subprocess.PIPE
        )
        await read_progress(process)

        await process.wait()
        self.emit('completed', process)

    def _build(self):
        arguments = [self._executable]
        arguments += build_options(self._global_options)

        for file in self._input_files:
            arguments += build_options(file.options)
            arguments += ['-i', file.url]

        for file in self._output_files:
            arguments += build_options(file.options)
            arguments += [file.url]

        return arguments
