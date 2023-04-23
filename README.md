# python-ffmpeg
A python binding for FFmpeg which provides sync and async APIs

## Help
See [documentation](https://python-ffmpeg.readthedocs.io) for more details.

## Install
To install **python-ffmpeg**, simply use pip:

```console
$ pip install python-ffmpeg
```

## Examples
You can find more examples in [the documentation](https://python-ffmpeg.readthedocs.io/).
### Transcoding
#### Synchronous API
```python
from ffmpeg import FFmpeg


def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("input.mp4")
        .output(
            "ouptut.mp4",
            {"codec:v": "libx264"},
            vf="scale=1280:-1",
            preset="veryslow",
            crf=24,
        )
    )

    ffmpeg.execute()


if __name__ == "__main__":
    main()
```

#### Asynchronous API
``` python
import asyncio

from ffmpeg.asyncio import FFmpeg


async def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("input.mp4")
        .output(
            "ouptut.mp4",
            {"codec:v": "libx264"},
            vf="scale=1280:-1",
            preset="veryslow",
            crf=24,
        )
    )

    await ffmpeg.execute()


if __name__ == "__main__":
    asyncio.run(main())
```

### Recording
#### Synchronous API
```python
from ffmpeg import FFmpeg, Progress


def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(
            "rtsp://username:password@127.0.0.1/cam",
            rtsp_transport="tcp",
            rtsp_flags="prefer_tcp",
        )
        .output("output.mp4", vcodec="copy")
    )

    @ffmpeg.on("progress")
    def time_to_terminate(progress: Progress):
        if progress.frame > 200:
            ffmpeg.terminate()

    ffmpeg.execute()


if __name__ == "__main__":
    main()
```

#### Asynchronous API
``` python
import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg


async def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(
            "rtsp://username:password@127.0.0.1/cam",
            rtsp_transport="tcp",
            rtsp_flags="prefer_tcp",
        )
        .output("output.mp4", vcodec="copy")
    )

    @ffmpeg.on("progress")
    def time_to_terminate(progress: Progress):
        if progress.frame > 200:
            ffmpeg.terminate()

    await ffmpeg.execute()


if __name__ == "__main__":
    asyncio.run(main())
```