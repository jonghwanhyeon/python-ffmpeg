# Monitoring status

In **python-ffmpeg**, the processing status of ffmpeg can be monitored through events. More information about the events can be found [here][events].

=== "Synchronous API"

    ```python
    from __future__ import annotations

    from ffmpeg import FFmpeg, Progress


    def main():
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("input.mp4")
            .output(
                "output.mp4",
                {"codec:v": "libx264"},
                vf="scale=1280:-1",
                preset="veryslow",
                crf=24,
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("started")
        def on_started(process: subprocess.Popen):
            print("process id: {process.pid}")
            os.setpriority(os.PRIO_PROCESS, process.pid, 10)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            print("stderr:", line)

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ``` python
    from __future__ import annotations

    import asyncio

    from ffmpeg import Progress
    from ffmpeg.asyncio import FFmpeg


    async def main():
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("input.mp4")
            .output(
                "output.mp4",
                {"codec:v": "libx264"},
                vf="scale=1280:-1",
                preset="veryslow",
                crf=24,
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("started")
        def on_started(process: subprocess.Popen):
            print("process id: {process.pid}")
            os.setpriority(os.PRIO_PROCESS, process.pid, 10)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            print("stderr:", line)

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        await ffmpeg.execute()


    if __name__ == "__main__":
        main()
    ```