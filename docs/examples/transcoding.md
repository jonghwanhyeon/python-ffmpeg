# Transcoding

You can use **python-ffmpeg** to transcode an input file into various codecs and formats.

For example, you can change the container of a video file without re-encoding the content as follows:

=== "Synchronous API"

    ```python
    from ffmpeg import FFmpeg, Progress


    def main():
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("input.mov")
            .output(
                "ouptut.mp4",
                codec="copy",
            )
        )

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        ffmpeg.execute()


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

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
                "ouptut.mp4",
                codec="copy",
            )
        )

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        await ffmpeg.execute()


    if __name__ == "__main__":
        asyncio.run(main())
    ```

You can also scale down the resolution of the video as follows.

=== "Synchronous API"

    ```python
    from ffmpeg import FFmpeg, Progress


    def main():
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("input.mov")
            .output(
                "ouptut.mp4",
                {"codec:v": "libx264", "filter:v": "scale=1280:-1"},
                preset="veryslow",
                crf=24,
            )
        )

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        ffmpeg.execute()


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

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
                "ouptut.mp4",
                {"codec:v": "libx264", "filter:v": "scale=1280:-1"},
                vf="scale=1280:-1",
                preset="veryslow",
                crf=24,
            )
        )

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        await ffmpeg.execute()


    if __name__ == "__main__":
        asyncio.run(main())
    ```