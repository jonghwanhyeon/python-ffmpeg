from __future__ import annotations

from typing_extensions import Self
import re

class FFmpegError(Exception):
    @classmethod
    def create(cls, error_message: str, command: str) -> Self:
        message = (
            f"{error_message}\n"
            f"Command: {command}"
        )

        error = error_message.lower()
        if "already exists" in error:
            raise FFmpegFileExists(message)
        elif "no such file" in error or "could not open file" in error:
            raise FFmpegFileNotFound(message)
        elif "unknown encoder" in error:
            raise FFmpegUnsupportedEncoder(message)
        elif any((
            "option not found" in error,
            "unrecognized option" in error,
            "trailing options were found on the commandline" in error,
            "invalid encoder type" in error,
            "codec not currently supported in container" in error,
            "option" in error and "not found" in error
            )):
            raise FFmpegInvalidCommand(message)
        else:
            raise FFmpegError(message)


class FFmpegAlreadyExecuted(FFmpegError):
    "FFmpeg was already run with this configuration and can only be executed once."


class FFmpegFileExists(FFmpegError):
    "The output file already exists, you can overwrite it using the -y option"


class FFmpegFileNotFound(FFmpegError):
    "An input file was not found"


class FFmpegInvalidCommand(FFmpegError):
    "FFmpeg was passed invalid options or arguments."


class FFmpegUnsupportedEncoder(FFmpegError):
    "FFmpeg attempted to encode using an unsupported encoder."
