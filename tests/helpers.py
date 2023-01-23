from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


def probe(path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "ffprobe",
            "-print_format", "json",  # fmt: skip
            "-show_streams",
            "-show_format",
            str(path.absolute()),
        ],
        capture_output=True,
    )

    if completed.returncode != 0:
        raise RuntimeError(f"An error occurred while probing {path}")

    return json.loads(completed.stdout)
