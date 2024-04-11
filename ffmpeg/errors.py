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

    def __init__(self, message: str, arguments: list[str]):
        super().__init__(message)

        self.message = message
        self.arguments = arguments

    @classmethod
    def create(cls, message: str, arguments: list[str]) -> Self:
        for subclass in cls.__subclasses__():
            if subclass._patterns is None:
                continue

            for pattern in subclass._patterns:
                if re.search(pattern, message, flags=re.IGNORECASE) is not None:
                    return subclass(message, arguments)

        return cls(message, arguments)


class FFmpegAlreadyExecuted(FFmpegError):
    "Represents FFmpeg is being executed"


class FFmpegFileNotFound(FFmpegError):
    "Represents an input file was not found"
    _patterns = [
        r"no such file",
        r"could not open file",
    ]


class FFmpegInvalidCommand(FFmpegError):
    "Represents FFmpeg was passed invalid options or arguments"
    _patterns = [
        r"option .* ?not found",
        r"unrecognized option",
        r"trailing options were found on the commandline",
        r"invalid encoder type",
        r"codec not currently supported in container",
    ]


class FFmpegUnsupportedCodec(FFmpegError):
    "Represents FFmpeg attempted to use an unsupported codec"
    _patterns = [
        r"unknown encoder",
        r"encoder not found",
        r"unknown decoder",
        r"decoder not found",
    ]
