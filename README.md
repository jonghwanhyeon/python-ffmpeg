

# python-ffmpeg
A python interface for FFmpeg using asyncio

## Requirements
- Python 3.5+
- pyee

## Installation
    pip install python-ffmpeg

## Usage
```python
import asyncio
from ffmpeg import FFmpeg

ffmpeg = FFmpeg().option('y').input(
    'rtsp://example.com/cam',
    # Specify file options using kwargs
    rtsp_transport='tcp',
    rtsp_flags='prefer_tcp',
).output(
    'output.ts',
    # Use a dictionary when an option name contains special characters
    {'codec:v': 'copy'},
    f='mpegts',
)

@ffmpeg.on('start')
def on_start(arguments):
    print('Arguments:', arguments)

@ffmpeg.on('stderr')
def on_stderr(line):
    print('stderr:', line)

@ffmpeg.on('progress')
def on_progress(progress):
    print(progress)

@ffmpeg.on('progress')
def time_to_terminate(progress):
    # Gracefully terminate when more than 200 frames are processed
    if progress.frame > 200:
        ffmpeg.terminate()

@ffmpeg.on('completed')
def on_completed():
    print('Completed')

@ffmpeg.on('terminated')
def on_terminated():
    print('Terminated')

@ffmpeg.on('error')
def on_error(code):
    print('Error:', code)

loop = asyncio.get_event_loop()
loop.run_until_complete(ffmpeg.execute())
loop.close()
```
## API
### FFmpeg
#### __init__(executable='ffmpeg')
- `executable`: the path to the ffmpeg executable

Initializes the `FFmpeg` instance.

#### option(key, value=None)
- `key`
- `value`

Specifies a global option `-key` or `-key value`

#### input(url, options=None, **kwargs)
- `url`
- `options`
- `kwargs`

Specifies an input file. An arbitrary number of input files can be specified by calling this method multiple times.

#### output(url, options=None, **kwargs)
- `url`
- `options`
- `kwargs`

Specifies an output file. An arbitrary number of output files can be specified by calling this method multiple times.

#### execute()
Executes FFmpeg using specified options and files.

#### terminate()
Gracefully terminates the running FFmpeg process.

#### on(event, listener=None)
- `event`: the name of the event
- `listener`: the callback function

Registers the `listener` to the `event`. This method can be used as a decorator.

#### Event: 'start'
- `arguments`: a sequence of arguments to execute FFmpeg

The `'start'` event is emitted just before FFmpeg is executed.

#### Event: 'stderr'
- `line`

The `'stderr'` event is emitted when FFmpeg writes a line to `stderr`.

#### Event: 'progress'
- `progress`: a namedtuple with `frame`, `fps`, `size`, `time`, `bitrate`, `speed` fields

The `'progress'` event is emitted when FFmpeg reports progress.

#### Event: 'completed'
The `'completed'` event is emitted when FFmpeg is successfully exited.

#### Event: 'terminated'
The `'terminated'` event is emitted when FFmpeg is terminated by calling `FFmpeg.terminate()`.

#### Event: 'error'
- `code`: a return code of the FFmpeg process

The `'error'` event is emitted when FFmpeg is exited with a non-zero return code
