# API Reference


::: ffmpeg
    options:
      members:
        - FFmpeg

::: ffmpeg.asyncio
    options:
      show_root_heading: true
      members:
        - FFmpeg

::: ffmpeg
    options:
      members:
        - Progress
        - FFmpegError

## Events
### `start`
This event is emitted just before `FFmpeg` is executed.

**Parameters:**

|    Name     |     Type    |               Description               |
|-------------|-------------|-----------------------------------------|
| `arguments` | `list[str]` | A list of arguments to execute `FFmpeg` |


### `stderr`
This event is emitted when a line is output to the standard error by `FFmpeg`.

**Parameters:**

|    Name     |  Type |          Description           |
|-------------|-------|--------------------------------|
|   `line`    | `str` | A line from the standard error |


### `progress`
This event is emitted when `FFmpeg` reports progress.

**Parameters:**

|    Name    |             Type              |           Description            |
|------------|-------------------------------|----------------------------------|
| `progress` | [`Progress`][ffmpeg.Progress] | A progress of `FFmpeg` operation |


### `completed`
This event is emitted when `FFmpeg` is successfully exited.

### `terminated`
This event is emitted when `FFmpeg` is gracefully terminated by calling `FFmpeg.terminate()`.