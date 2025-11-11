import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Définir RUN_INTEGRATION_TESTS=1 pour exécuter les tests d'intégration.",
)
def test_docker_compose_configuration_is_valid():
    """Valide la configuration docker-compose en mode smoke-test."""
    cmd = ["docker", "compose", "config"]
    completed = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        pytest.fail(f"docker compose config a échoué\n{completed.stdout}")
