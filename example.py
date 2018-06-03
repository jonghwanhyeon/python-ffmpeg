import asyncio

from ffmpeg import FFmpeg

ffmpeg = FFmpeg().global_option('y').input_file(
    'input.mp4',
    f='mp4',
).output_file(
    'output.mp4',
    map=0,
    c='copy',
    c__v__1='libx264',
    c__a__137='libvorbis'
)


@ffmpeg.on('progress')
def on_progress(process, progress):
    print(progress)


@ffmpeg.on('completed')
def on_completed(process):
    print('Done', process.returncode)


loop = asyncio.get_event_loop()
loop.run_until_complete(ffmpeg.run())
loop.close()
