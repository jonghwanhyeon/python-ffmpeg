# Asynchronous Listeners

When using the Asynchronous API, event listeners may be either regular functions or coroutines.

``` python
import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg


async def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("input.mov")
        .output(
            "output.mp4",
            codec="copy",
        )
    )

    @ffmpeg.on("progress")
    async def on_progress(progress: Progress):
        await asyncio.sleep(1)
        print(progress)

    @ffmpeg.on("completed")
    def on_completed():
        print("Completed")

    await ffmpeg.execute()


if __name__ == "__main__":
    asyncio.run(main())
```
