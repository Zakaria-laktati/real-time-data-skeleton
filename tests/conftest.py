import sys
import sys
import types
import typing
from pathlib import Path
from typing import IO

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if "typing.io" not in sys.modules:
    typing_io = types.ModuleType("typing.io")
    typing_io.BinaryIO = IO[bytes]
    typing_io.TextIO = IO[str]
    sys.modules["typing.io"] = typing_io
    typing.io = typing_io  # type: ignore[attr-defined]
    sys.modules["typing.io"] = typing_io

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Crée une session Spark locale pour les tests unitaires."""
    session = (
        SparkSession.builder.appName("pytest-real-time-pipeline")
        .master("local[2]")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("WARN")
    yield session
    session.stop()
