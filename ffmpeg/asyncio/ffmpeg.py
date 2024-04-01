from __future__ import annotations

import asyncio
import io
import os
import signal
import subprocess
from typing import Optional, Union, AsyncIterable

from pyee.asyncio import AsyncIOEventEmitter
from typing_extensions import Self

from ffmpeg import types
from ffmpeg.asyncio.utils import create_subprocess, ensure_stream_reader, read_stream, readlines
from ffmpeg.ffmpeg import FFmpegAlreadyExecuted, FFmpegError
from ffmpeg.options import Options
from ffmpeg.progress import Tracker
from ffmpeg.utils import is_windows


class FFmpeg(AsyncIOEventEmitter):
    def __init__(self, executable: str = "ffmpeg"):
        """Initialize an `FFmpeg` instance using `asyncio`

        Args:
            executable: The path to the ffmpeg executable. Defaults to "ffmpeg".
        """
        super().__init__()

        self._executable: str = executable
        self._options: Options = Options()

        self._process: asyncio.subprocess.Process
        self._executed: bool = False
        self._terminated: bool = False
        self._tasks = {}

        self._tracker = Tracker(self)  # type: ignore

        self.once("error", self._reraise_exception)

    @property
    def arguments(self) -> list[str]:
        """Return a list of arguments to be used when executing FFmpeg.

        Returns:
            A lit of arguments to be used when executing FFmpeg.
        """
        return [self._executable, *self._options.build()]

    def option(self, key: str, value: Optional[types.Option] = None) -> Self:
        """Add a global option `-key` or `-key value`.

        Args:
            key: A key of the global option
            value: A value of the global option. If the option does not require a value, use None. Defaults to None.

        Returns:
            An instance of `FFmpeg` itself, so that calls can be chained.
        """
        self._options.option(key, value)
        return self

    def input(
        self,
        url: Union[str, os.PathLike],
        options: Optional[dict[str, Optional[types.Option]]] = None,
        **kwargs: Optional[types.Option],
    ) -> Self:
        """Add an input file with specified options.
           By calling this method multiple times, an arbitrary number of input files can be added.

        Args:
            url: URL for the input file.
            options: Options for the input file. Defaults to None.
            kwargs: Additional options for the input file.

        Note:
            Options for an input file can be specified in two ways:

            Using `options`:
            ```python
            ffmpeg = FFmpeg().input("input.mp4", {"codec:v": "libx264"}).output("output.mp4")
            # Corresponds to `ffmpeg -codec:v libx264 -i input.mp4 output.mp4`
            ```

            Using `**kwargs`:
            ```python
            ffmpeg = FFmpeg().input("input.mp4", vcodec="libx264").output("output.mp4")
            # Corresponds to `ffmpeg -vcodec libx264 -i input.mp4 output.mp4`
            ```

        Note:
            If an option does not require a value, use `None` for its value.

            ```python
            ffmpeg = FFmpeg().input("input.mp4", ignore_unknown=None).output("output.mp4")
            # Corresponds to `ffmpeg -ignore_unknown -i input.mp4 output.mp4`
            ```

        Returns:
            An instance of `FFmpeg` itself, so that calls can be chained.
        """
        self._options.input(url, options, **kwargs)
        return self

    def output(
        self,
        url: Union[str, os.PathLike],
        options: Optional[dict[str, Optional[types.Option]]] = None,
        **kwargs: Optional[types.Option],
    ) -> Self:
        """Add an output file with specified options.
           By calling this method multiple times, an arbitrary number of output files can be specified.

        Args:
            url: URL for the output file.
            options: Options for the output file. Defaults to None.
            kwargs: Additional options for the output file.

        Note:
            Options for an output file can be specified in two ways:

            Using `options`:
            ```python
            ffmpeg = FFmpeg().input("input.mp4").output("output.mp4", {"codec:v": "libx264"})
            # Corresponds to `ffmpeg -i input.mp4 -codec:v libx264 output.mp4`
            ```

            Using `**kwargs`:
            ```python
            ffmpeg = FFmpeg().input("input.mp4").output("output.mp4", vcodec="libx264")
            # Corresponds to `ffmpeg -i input.mp4 -vcodec libx264 output.mp4`
            ```

        Note:
            If an option does not require a value, use `None` for its value.

            ```python
            ffmpeg = FFmpeg().input("input.mp4").output("output.mp4", ignore_unknown=None)
            # Corresponds to `ffmpeg -i input.mp4 -ignore_unknown output.mp4`
            ```

        Returns:
            An instance of `FFmpeg` itself, so that calls can be chained.
        """
        self._options.output(url, options, **kwargs)
        return self

    async def _start_execution(self, stream: Optional[Union[bytes, asyncio.StreamReader]] = None):
        if self._executed:
            raise FFmpegAlreadyExecuted("FFmpeg is already executed", arguments=self.arguments)

        self._executed = False
        self._terminated = False

        self.emit("start", self.arguments)

        self._process = await create_subprocess(
            *self.arguments,
            stdin=subprocess.PIPE if stream is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self._executed = True

    async def _wait_for_execution(self):
        done, pending = await asyncio.wait(self._tasks.values(), return_when=asyncio.FIRST_EXCEPTION)
        self._executed = False

        for task in done:
            exception = task.exception()
            if exception is not None:
                self._process.terminate()
                for task in pending:
                    await task

                raise exception

        if self._process.returncode == 0:
            self.emit("completed")
        elif self._terminated:
            self.emit("terminated")
        else:
            raise FFmpegError.create(message=self._tasks["stderr"].result(), arguments=self.arguments)

    async def execute(
            self, stream: Optional[Union[bytes, asyncio.StreamReader]] = None, timeout: Optional[float] = None,
    ) -> bytes:
        """Execute FFmpeg using specified global options and files.

        Args:
            stream: A stream to input to the standard input. Defaults to None.
            timeout: The maximum number of seconds to wait before returning. Defaults to None.

        Raises:
            FFmpegAlreadyExecuted: If FFmpeg is already executed.
            FFmpegError: If FFmpeg process returns non-zero exit status.
            asyncio.TimeoutError: If FFmpeg process does not terminate after `timeout` seconds.

        Returns:
            The output to the standard output.
        """
        if stream is not None:
            stream = ensure_stream_reader(stream)
        await self._start_execution(stream=stream)

        self._tasks = {
            "stdin": asyncio.create_task(self._write_stdin(stream)),
            "stdout": asyncio.create_task(self._read_stdout()),
            "stderr": asyncio.create_task(self._handle_stderr()),
            "main": asyncio.create_task(asyncio.wait_for(self._process.wait(), timeout=timeout)),
        }

        await self._wait_for_execution()
        return self._tasks["stdout"].result()

    async def execute_stream_stdout(
            self, stream: Optional[Union[bytes, asyncio.StreamReader]] = None, timeout: Optional[float] = None,
            *, stream_chunk_size=io.DEFAULT_BUFFER_SIZE
    ) -> AsyncIterable[bytes]:
        """Like `execute`, but returns a generator of bytes, so you can read the output as it starts to come out."""
        if stream is not None:
            stream = ensure_stream_reader(stream)
        await self._start_execution(stream=stream)
        self._tasks = {
            "stdin": asyncio.create_task(self._write_stdin(stream)),
            "stderr": asyncio.create_task(self._handle_stderr()),
            "main": asyncio.create_task(asyncio.wait_for(self._process.wait(), timeout=timeout)),
        }
        async for chunk in read_stream(self._process.stdout, size=stream_chunk_size):
            yield chunk
        await self._wait_for_execution()

    def terminate(self):
        """Gracefully terminate the running FFmpeg process.

        Raises:
            FFmpegError: If FFmpeg is not executed
        """
        if not self._executed:
            raise FFmpegError("FFmpeg is not executed", arguments=self.arguments)

        sigterm = signal.SIGTERM
        if is_windows():
            # On Windows, SIGTERM is an alias for TerminateProcess().
            # To gracefully terminate the FFmpeg process, we should use CTRL_BREAK_EVENT signal.
            # References:
            # - https://docs.python.org/3.10/library/subprocess.html#subprocess.Popen.send_signal
            # - https://github.com/FFmpeg/FFmpeg/blob/release/5.1/fftools/ffmpeg.c#L371
            sigterm = signal.CTRL_BREAK_EVENT  # type: ignore

        self._terminated = True
        self._process.send_signal(sigterm)

    async def _write_stdin(self, stream: Optional[asyncio.StreamReader]):
        if stream is None:
            return

        assert self._process.stdin is not None

        async for chunk in read_stream(stream, size=io.DEFAULT_BUFFER_SIZE):
            self._process.stdin.write(chunk)
            await self._process.stdin.drain()

        self._process.stdin.close()
        await self._process.stdin.wait_closed()

    async def _read_stdout(self) -> bytes:
        assert self._process.stdout is not None

        buffer = bytearray()
        async for chunk in read_stream(self._process.stdout, size=io.DEFAULT_BUFFER_SIZE):
            buffer.extend(chunk)

        return bytes(buffer)

    async def _handle_stderr(self) -> str:
        assert self._process.stderr is not None

        line = b""
        async for line in readlines(self._process.stderr):
            self.emit("stderr", line.decode())

        return line.decode()

    def _reraise_exception(self, exception: Exception):
        raise exception
