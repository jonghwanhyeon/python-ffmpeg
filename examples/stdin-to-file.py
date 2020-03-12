import asyncio
from ffmpeg import FFmpeg

ffmpeg = FFmpeg().option('y').input('pipe:0').output(
    'ouptut.mp4',
    c='copy'
)

@ffmpeg.on('start')
def on_start(arguments):
    print('arguments:', arguments)


@ffmpeg.on('stderr')
def on_stderr(line):
    print('stderr:', line)


@ffmpeg.on('progress')
def on_progress(progress):
    print(progress)

@ffmpeg.on('completed')
def on_completed():
    print('completed')


@ffmpeg.on('terminated')
def on_terminated():
    print('terminated')


@ffmpeg.on('error')
def on_error(code):
    print('error:', code)


async def main():
    streamlink = await asyncio.create_subprocess_exec(
        'streamlink',
        '--stdout',
        'https://www.twitch.tv/hanryang1125',
        'best',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )

    await ffmpeg.execute(streamlink.stdout)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
