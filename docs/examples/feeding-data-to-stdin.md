# Feeding data to `stdin`

You can use **python-ffmpeg** to directly input data into ffmpeg's `stdin`. In this case, you can pass the input data as an argument of [`FFmpeg.execute()`][ffmpeg.FFmpeg.execute].

!!! note

    To feed data to ffmpeg's `stdin`, you must use `pipe:0` as the URL for the input file.

If the data to be input is stored in memory as bytes, you can pass it to ffmpeg as follows:

=== "Synchronous API"

    ```python
    from pathlib import Path

    from ffmpeg import FFmpeg, Progress


    def main():
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("pipe:0")
            .output(
                "input.mp4",
                codec="copy",
            )
        )

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        ffmpeg.execute(Path("input.ts").read_bytes())


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ``` python
    import asyncio
    from pathlib import Path

    from ffmpeg import Progress
    from ffmpeg.asyncio import FFmpeg


    async def main():
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("pipe:0")
            .output(
                "input.mp4",
                codec="copy",
            )
        )

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        await ffmpeg.execute(Path("input.ts").read_bytes())


    if __name__ == "__main__":
        asyncio.run(main())
    ```

You can also feed the output of another stream (such as a file or the `stdout` of another process) to ffmpeg's `stdin` as follows:

=== "Synchronous API"

    ```python
    import subprocess

    from ffmpeg import FFmpeg, Progress


    def main():
        streamlink = subprocess.Popen(
            ["streamlink", "--stdout", "https://twitch.tv/zilioner", "best"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        ffmpeg = FFmpeg().option("y").input("pipe:0").output("output.mp4", c="copy")

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        ffmpeg.execute(streamlink.stdout)


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ``` python
    import asyncio

    from ffmpeg import Progress
    from ffmpeg.asyncio import FFmpeg


    async def main():
        streamlink = await asyncio.create_subprocess_exec(
            "streamlink",
            "--stdout",
            "https://twitch.tv/zilioner",
            "best",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )

        ffmpeg = FFmpeg().option("y").input("pipe:0").output("output.mp4", c="copy")

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        await ffmpeg.execute(streamlink.stdout)


    if __name__ == "__main__":
        asyncio.run(main())

    ```