# Handling errors

If an error occurs during ffmpeg's execution, you can use `try: except:` to get more information about the error.

=== "Synchronous API"

    ```python
    from ffmpeg import FFmpeg, FFmpegFileNotFound, FFmpegInvalidCommand


    def main():
        try:
            ffmpeg = FFmpeg().input("non-existent.mp4").output("output.mp4")
            ffmpeg.execute()
        except FFmpegFileNotFound as exception:
            print("An exception has been occurred!")
            print("- Message from ffmpeg:", exception.message)
            print("- Arguments to execute ffmpeg:", exception.arguments)

        try:
            ffmpeg = FFmpeg().input("input.mp4", invalid="option").output("output.mp4")
            ffmpeg.execute()
        except FFmpegInvalidCommand as exception:
            print("An exception has been occurred!")
            print("- Message from ffmpeg:", exception.message)
            print("- Arguments to execute ffmpeg:", exception.arguments)


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ``` python
    import asyncio

    from ffmpeg import FFmpegFileNotFound, FFmpegInvalidCommand
    from ffmpeg.asyncio import FFmpeg


    async def main():
        try:
            ffmpeg = FFmpeg().input("non-existent.mp4").output("output.mp4")
            await ffmpeg.execute()
        except FFmpegFileNotFound as exception:
            print("An exception has been occurred!")
            print("- Message from FFmpeg:", exception.message)
            print("- Arguments to execute ffmpeg:", exception.arguments)

        try:
            ffmpeg = FFmpeg().input("input.mp4", invalid="option").output("output.mp4")
            await ffmpeg.execute()
        except FFmpegInvalidCommand as exception:
            print("An exception has been occurred!")
            print("- Message from FFmpeg:", exception.message)
            print("- Arguments to execute ffmpeg:", exception.arguments)


    if __name__ == "__main__":
        asyncio.run(main())

    ```