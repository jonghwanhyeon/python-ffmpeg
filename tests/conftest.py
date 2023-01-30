from __future__ import annotations

import sys
from pathlib import Path

import pytest

tests_path = Path(__file__).parent.absolute()
sys.path.append(str(tests_path))


@pytest.fixture
def assets_path() -> Path:
    return tests_path / "assets"
