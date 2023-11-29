from __future__ import annotations

import re
from typing import ClassVar, Optional

from typing_extensions import Self


class FFmpegError(Exception):
    """Represents an error that has occurred during `FFmpeg` operation.

    Attributes:
        message: An error message providing details about the error.
        arguments: Arguments passed to FFmpeg.
    """

    _patterns: ClassVar[Optional[list[str]]] = None

    def __init__(self, message: str, arguments: Optional[list[str]] = None):
        super().__init__(message)

        self.message = message
        self.arguments = arguments

    @classmethod
    def create(cls, message: str, arguments: Optional[list[str]] = None) -> Self:
        for subclass in cls.__subclasses__():
            if subclass._patterns is None:
                continue

            for pattern in subclass._patterns:
                if re.search(pattern, message, flags=re.IGNORECASE) is not None:
                    return subclass(message, arguments)

        return FFmpegError(message, arguments)


class FFmpegAlreadyExecuted(FFmpegError):
    "FFmpeg is being executed"


class FFmpegFileExists(FFmpegError):
    "The output file already exists, you can overwrite it using the -y option"
    _patterns = [
        r"already exists",
    ]


class FFmpegFileNotFound(FFmpegError):
    "An input file was not found"
    _patterns = [
        r"no such file",
        r"could not open file",
    ]


class FFmpegInvalidCommand(FFmpegError):
    "FFmpeg was passed invalid options or arguments"
    _patterns = [
        r"option .* ?not found",
        r"unrecognized option",
        r"trailing options were found on the commandline",
        r"invalid encoder type",
        r"codec not currently supported in container",
    ]


class FFmpegUnsupportedCodec(FFmpegError):
    "FFmpeg attempted to use an unsupported codec"
    _patterns = [
        r"unknown encoder",
        r"unknown decoder",
    ]
