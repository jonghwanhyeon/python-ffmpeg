import asyncio

from ffmpeg import FFmpeg


async def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("rtsp://127.0.0.1/cam", rtsp_transport="tcp", rtsp_flags="prefer_tcp")
        .output("otuput.mp4", vcodec="copy")
    )

    @ffmpeg.on("start")
    def on_start(arguments):
        print("arguments:", arguments)

    @ffmpeg.on("stderr")
    def on_stderr(line):
        print("stderr:", line)

    @ffmpeg.on("progress")
    def on_progress(progress):
        print(progress)

    @ffmpeg.on("progress")
    def time_to_terminate(progress):
        if progress.frame > 200:
            ffmpeg.terminate()

    @ffmpeg.on("completed")
    def on_completed():
        print("completed")

    @ffmpeg.on("terminated")
    def on_terminated():
        print("terminated")

    @ffmpeg.on("error")
    def on_error(code):
        print("error:", code)

    await ffmpeg.execute()


if __name__ == "__main__":
    asyncio.run(main())
