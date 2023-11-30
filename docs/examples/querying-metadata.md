# Querying metadata

You can use **python-ffmpeg** to query the metadata of an input file using `ffprobe`.

=== "Synchronous API"

    ```python
    import json

    from ffmpeg import FFmpeg


    def main():
        ffprobe = FFmpeg(executable="ffprobe").input(
            "input.mp4",
            print_format="json", # ffprobe will output the results in JSON format
            show_streams=None,
        )

        media = json.loads(ffprobe.execute())

        print(f"# Video")
        print(f"- Codec: {media['streams'][0]['codec_name']}")
        print(f"- Resolution: {media['streams'][0]['width']} X {media['streams'][0]['height']}")
        print(f"- Duration: {media['streams'][0]['duration']}")
        print("")

        print(f"# Audio")
        print(f"- Codec: {media['streams'][1]['codec_name']}")
        print(f"- Sample Rate: {media['streams'][1]['sample_rate']}")
        print(f"- Duration: {media['streams'][1]['duration']}")


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ``` python
    import asyncio
    import json

    from ffmpeg.asyncio import FFmpeg


    async def main():
        ffprobe = FFmpeg(executable="ffprobe").input(
            "input.mp4",
            print_format="json", # ffprobe will output the results in JSON format
            show_streams=None,
        )

        media = json.loads(await ffprobe.execute())

        print(f"# Video")
        print(f"- Codec: {media['streams'][0]['codec_name']}")
        print(f"- Resolution: {media['streams'][0]['width']} X {media['streams'][0]['height']}")
        print(f"- Duration: {media['streams'][0]['duration']}")
        print("")

        print(f"# Audio")
        print(f"- Codec: {media['streams'][1]['codec_name']}")
        print(f"- Sample Rate: {media['streams'][1]['sample_rate']}")
        print(f"- Duration: {media['streams'][1]['duration']}")


    if __name__ == "__main__":
        asyncio.run(main())
    ```