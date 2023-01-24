# Mapping multiple input files

When you have two media files, you can use only video in one media file and only audio in the other as follows.

=== "Synchronous API"

    ```python
    import subprocess

    from ffmpeg import FFmpeg, Progress


    def main():
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("input-a.mp4")
            .input("input-b.mp4")
            .output(
                "output.mp4",
                map=["0:0", "1:1"],
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
            .input("input-a.mp4")
            .input("input-b.mp4")
            .output(
                "output.mp4",
                map=["0:0", "1:1"],
            )
        )

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        await ffmpeg.execute()


    if __name__ == "__main__":
        asyncio.run(main())

    ```