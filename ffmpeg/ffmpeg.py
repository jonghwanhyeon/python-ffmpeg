from __future__ import annotations

import asyncio
import signal
import sys
from codecs import StreamReader
from collections import namedtuple
from typing import Dict, List, Optional

from pyee import EventEmitter

from ffmpeg.typing import Option
from ffmpeg.utils import build_options, parse_progress, readlines

_windows = sys.platform == "win32"


def _create_subprocess(*args, **kwargs) -> asyncio.subprocess.Process:
    if _windows:
        # https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.asyncio.subprocess.Process.send_signal
        from subprocess import CREATE_NEW_PROCESS_GROUP

        kwargs["creationflags"] = CREATE_NEW_PROCESS_GROUP

    return asyncio.create_subprocess_exec(*args, **kwargs)


class FFmpegError(Exception):
    pass


class FFmpeg(EventEmitter):
    _File = namedtuple("_File", ["url", "options"])

    def __init__(self, executable: str = "ffmpeg", skip_default_drain: bool = False):
        super().__init__()

        self._executable = executable
        self._global_options = {}
        self._input_files = []
        self._output_files = []

        self._executed = False
        self._terminated = False
        self._process = None
        self._skip_default_drain = skip_default_drain

        self.on("stderr", self._on_stderr)

    def option(self, key: str, value: Optional[Option] = None) -> FFmpeg:
        self._global_options[key] = value
        return self

    def input(self, url: str, options: Optional[Dict[str, Option]] = None, **kwargs) -> FFmpeg:
        if options is None:
            options = {}

        self._input_files.append(FFmpeg._File(url=url, options={**options, **kwargs}))
        return self

    def output(self, url: str, options: Optional[Dict[str, Option]] = None, **kwargs) -> FFmpeg:
        if options is None:
            options = {}

        self._output_files.append(FFmpeg._File(url=url, options={**options, **kwargs}))
        return self

    async def execute(self, stream: Optional[asyncio.StreamReader] = None):
        if self._executed:
            raise FFmpegError("FFmpeg is already executed")

        arguments = self._build()
        self.emit("start", arguments)

        self._process = await _create_subprocess(
            *arguments,
            stdin=asyncio.subprocess.PIPE if stream is not None else None,
            stderr=asyncio.subprocess.PIPE,
        )

        self._executed = True
        await asyncio.wait(
            [
                asyncio.create_task(self._write_stdin(stream)),
                asyncio.create_task(self._read_stderr()),
                asyncio.create_task(self._process.wait()),
            ]
        )

        if self._process.returncode == 0:
            self.emit("completed")
        elif self._terminated:
            self.emit("terminated")
        else:
            self.emit("error", self._process.returncode)

    def terminate(self):
        if not self._executed:
            raise FFmpegError("FFmpeg is not executed")

        sigterm = signal.SIGTERM
        if _windows:  # On Windows, SIGTERM -> TerminateProcess()
            # https://github.com/FFmpeg/FFmpeg/blob/master/fftools/ffmpeg.c#L356
            sigterm = signal.CTRL_BREAK_EVENT

        self._terminated = True
        self._process.send_signal(sigterm)

    async def drain(self):
        # Memory leak occurs when too much data is feed to StreamReader (stream)
        # So expe StreamWriter's (stdin) drain to be called to create back pressure
        return await self._process.stdin.drain()

    async def _write_stdin(self, stream: Optional[StreamReader]):
        if stream is None:
            return

        while not stream.at_eof():
            self._process.stdin.write(await stream.read(1024))
            if not self._skip_default_drain:
                await self._process.stdin.drain()
        self._process.stdin.write_eof()

    async def _read_stderr(self):
        async for line in readlines(self._process.stderr):
            self.emit("stderr", line.decode("utf-8"))

    def _on_stderr(self, line: str):  # registered in __init__()
        progress = parse_progress(line)
        if progress:
            self.emit("progress", progress)

    def _build(self) -> List[str]:
        arguments = [self._executable]
        arguments.extend(build_options(self._global_options))

        for file in self._input_files:
            arguments.extend(build_options(file.options))
            arguments.extend(["-i", file.url])

        for file in self._output_files:
            arguments.extend(build_options(file.options))
            arguments.append(file.url)

        return arguments
