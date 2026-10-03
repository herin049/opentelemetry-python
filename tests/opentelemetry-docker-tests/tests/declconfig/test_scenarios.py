# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from opentelemetry.test._otlp_test_server import OtlpProtoTestServer

_SCENARIOS_DIR = Path(__file__).parent / "scenarios"
_SCENARIOS = sorted(path for path in _SCENARIOS_DIR.iterdir() if path.is_dir())
_RUN_TIMEOUT = 60.0
_TELEMETRY_TIMEOUT = 10.0


@pytest.mark.parametrize("scenario", _SCENARIOS, ids=[path.name for path in _SCENARIOS])
def test_scenario(scenario: Path, collector: str, otlp_sink: OtlpProtoTestServer) -> None:
    instrument = shutil.which("opentelemetry-instrument")
    assert instrument is not None, "opentelemetry-instrument is not installed"

    result = subprocess.run(
        [instrument, sys.executable, "run.py"],
        cwd=scenario,
        env={
            **os.environ,
            "OTEL_CONFIG_FILE": str(scenario / "otel-config.yaml"),
            "OTEL_COLLECTOR_ENDPOINT": collector,
        },
        capture_output=True,
        text=True,
        timeout=_RUN_TIMEOUT,
        check=False,
    )
    assert result.returncode == 0, f"run.py failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"

    with open(scenario / "expected.yaml", encoding="utf-8") as expected_file:
        expected = yaml.safe_load(expected_file)

    # TODO: compare against expected.yaml once its schema is defined.
    if not expected:
        otlp_sink.get_span(timeout=_TELEMETRY_TIMEOUT)
