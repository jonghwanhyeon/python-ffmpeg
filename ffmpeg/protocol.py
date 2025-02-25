from __future__ import annotations

import os
from typing import Any, Awaitable, Callable, Final, Optional, Protocol, TypeVar, Union

from typing_extensions import Self, TypeAlias

from ffmpeg import types

SyncExecute: TypeAlias = Callable[[Optional[types.Stream], Optional[float]], bytes]
AsyncExecute: TypeAlias = Callable[[Optional[types.AsyncStream], Optional[float]], Awaitable[bytes]]
ExecuteType_co = TypeVar("ExecuteType_co", SyncExecute, AsyncExecute, covariant=True)


class FFmpegProtocol(Protocol[ExecuteType_co]):
    def __init__(self, executable: str = "ffmpeg"): ...

    @property
    def arguments(self) -> list[str]: ...

    def option(self, key: str, value: Optional[types.Option] = None) -> Self: ...

    def input(
        self,
        url: Union[str, os.PathLike[str]],
        options: Optional[dict[str, Optional[types.Option]]] = None,
        **kwargs: Optional[types.Option],
    ) -> Self: ...

    def output(
        self,
        url: Union[str, os.PathLike[str]],
        options: Optional[dict[str, Optional[types.Option]]] = None,
        **kwargs: Optional[types.Option],
    ) -> Self: ...

    execute: Final[ExecuteType_co]

    def terminate(self): ...

    def on(
        self, event: str, f: Optional[types.Handler] = None
    ) -> Union[types.Handler, Callable[[types.Handler], types.Handler]]: ...

    def emit(self, event: str, *args: Any, **kwargs: Any) -> bool: ...
