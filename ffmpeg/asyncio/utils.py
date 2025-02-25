import asyncio
import io
import re
import subprocess
import sys
from functools import wraps
from typing import Any, AsyncIterable

from ffmpeg import types


@wraps(asyncio.create_subprocess_exec)
def create_subprocess(*args: Any, creationflags: int = 0, **kwargs: Any):
    # On Windows, CREATE_NEW_PROCESS_GROUP flag is required to use CTRL_BREAK_EVENT signal,
    # which is required to gracefully terminate the FFmpeg process.
    # Reference: https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.subprocess.Process.send_signal
    if sys.platform == "win32":
        creationflags |= subprocess.CREATE_NEW_PROCESS_GROUP

    return asyncio.create_subprocess_exec(*args, creationflags=creationflags, **kwargs)


async def read_bytes(stream: bytes, size: int = -1) -> AsyncIterable[bytes]:
    if size == -1:
        yield stream
        return

    for i in range(0, len(stream), size):
        yield stream[i : i + size]


async def read_stream(stream: asyncio.StreamReader, size: int = -1) -> AsyncIterable[bytes]:
    while not stream.at_eof():
        chunk = await stream.read(size)
        if not chunk:
            break

        yield chunk


def ensure_async_iterable(stream: types.AsyncStream) -> AsyncIterable[bytes]:
    if isinstance(stream, bytes):
        return read_bytes(stream, io.DEFAULT_BUFFER_SIZE)

    if isinstance(stream, asyncio.StreamReader):
        return read_stream(stream, io.DEFAULT_BUFFER_SIZE)

    return stream


async def readlines(stream: asyncio.StreamReader) -> AsyncIterable[bytes]:
    pattern = re.compile(rb"[\r\n]+")

    buffer = bytearray()
    async for chunk in read_stream(stream, io.DEFAULT_BUFFER_SIZE):
        buffer.extend(chunk)

        lines = pattern.split(buffer)
        buffer[:] = lines.pop(-1)  # keep the last line that could be partial

        for line in lines:
            yield line

    if buffer:
        yield bytes(buffer)
