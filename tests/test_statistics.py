from datetime import timedelta

from ffmpeg.statistics import Statistics


def test_statistics():
    assert Statistics.from_line(
        "size=     243kB time=00:01:01.47 bitrate=  32.4kbits/s speed= 123x",
    ) == Statistics(
        frame=0,
        fps=0.0,
        size=243 * 1024,
        time=timedelta(minutes=1, seconds=1, microseconds=470000),
        bitrate=32.4,
        speed=123,
    )

    assert Statistics.from_line(
        "frame=    0 fps=0.0 q=0.0 size=       0kB time=00:00:00.33 bitrate=   1.1kbits/s speed=22.8x",
    ) == Statistics(
        frame=0,
        fps=0.0,
        size=0,
        time=timedelta(microseconds=330000),
        bitrate=1.1,
        speed=22.8,
    )

    assert Statistics.from_line(
        "frame=  109 fps=0.0 q=-1.0 Lsize=     793kB time=00:00:04.02 bitrate=N/A speed=N/A",
    ) == Statistics(
        frame=109,
        fps=0.0,
        size=793 * 1024,
        time=timedelta(seconds=4, microseconds=20000),
        bitrate=0,
        speed=0,
    )

    assert Statistics.from_line(
        "frame=  109 fps=0.0 q=-1.0 Lsize=     793kB time=00:00:04.02 bitrate=1613.7kbits/s speed=7.73x",
    ) == Statistics(
        frame=109,
        fps=0.0,
        size=793 * 1024,
        time=timedelta(seconds=4, microseconds=20000),
        bitrate=1613.7,
        speed=7.73,
    )

    assert (
        Statistics.from_line(
            "configuration: --pkg-config-flags=--static --extra-cflags=-fopenmp --extra-ldflags='-fopenmp -Wl,-z,stack-size=2097152' --toolchain=hardened",
        )
        == None
    )
