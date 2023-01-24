# Recording

You can use **python-ffmpeg** to record a remote stream to a file. For example, when there is a surveillance camera supporting the `rstp` protocol, a video can be recorded in a file as follows.

=== "Synchronous API"

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
            # If you have recorded more than 200 frames, stop recording
            if progress.frame > 200:
                ffmpeg.terminate()

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
            .input(
                "rtsp://username:password@127.0.0.1/cam",
                rtsp_transport="tcp",
                rtsp_flags="prefer_tcp",
            )
            .output("output.mp4", vcodec="copy")
        )

        @ffmpeg.on("progress")
        def time_to_terminate(progress: Progress):
            # If you have recorded more than 200 frames, stop recording
            if progress.frame > 200:
                ffmpeg.terminate()

        await ffmpeg.execute()


    if __name__ == "__main__":
        asyncio.run(main())
    ```