# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Generator

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
SRC_PATH = PROJECT_ROOT / "src"
PROTO_PATH = Path(__file__).parent / "proto"
GEN_PATH = Path(__file__).parent / "generated"


@pytest.fixture(scope="module", autouse=True)
def generate_code() -> Generator[None, None, None]:
    if GEN_PATH.exists():
        shutil.rmtree(GEN_PATH)
    GEN_PATH.mkdir(parents=True)

    wrapper_path = PROJECT_ROOT / "protoc-gen-otlp_json_wrapper.py"
    wrapper_content = f"""#!/usr/bin/env python3
from opentelemetry.codegen.json.plugin import main
if __name__ == "__main__":
    main()
"""
    wrapper_path.write_text(wrapper_content)
    wrapper_path.chmod(0o755)

    try:
        protos = list(PROTO_PATH.glob("**/*.proto"))
        proto_files = [str(p.relative_to(PROTO_PATH)) for p in protos]

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "grpc_tools.protoc",
                f"-I{PROTO_PATH}",
                f"--plugin=protoc-gen-otlp_json={wrapper_path}",
                f"--otlp_json_out={GEN_PATH}",
                *proto_files,
            ]
        )

        sys.path.insert(0, str(GEN_PATH.absolute()))
        yield
    finally:
        if wrapper_path.exists():
            wrapper_path.unlink()


def test_generated_message_roundtrip() -> None:
    from otel_test_json.test.v1.test import TestMessage, SubMessage  # type: ignore

    msg = TestMessage(
        name="test",
        int_value=123,
        bool_value=True,
        double_value=1.5,
        int64_value=9223372036854775807,
        uint64_value=18446744073709551615,
        bytes_value=b"hello",
        trace_id=b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\x0d\x0e\x0f",
        span_id=b"\x00\x01\x02\x03\x04\x05\x06",
        list_strings=["a", "b"],
        list_ints=[1, 2],
        enum_value=TestMessage.TestEnum.SUCCESS,
        sub_message=SubMessage(content="sub"),
        list_messages=[SubMessage(content="m1"), SubMessage(content="m2")],
        oneof_string="oneof",
    )

    json_str = msg.to_json()
    data = json.loads(json_str)

    assert data["name"] == "test"
    assert data["intValue"] == 123
    assert data["boolValue"] is True
    assert data["doubleValue"] == 1.5
    assert data["int64Value"] == "9223372036854775807"
    assert data["uint64Value"] == "18446744073709551615"
    assert data["bytesValue"] == "aGVsbG8="
    assert data["traceId"] == "000102030405060708090a0b0c0d0e0f"
    assert data["spanId"] == "00010203040506"
    assert data["listStrings"] == ["a", "b"]
    assert data["listInts"] == [1, 2]
    assert data["enumValue"] == 1
    assert data["subMessage"]["content"] == "sub"
    assert len(data["listMessages"]) == 2
    assert data["oneofString"] == "oneof"
    assert "oneofInt" not in data

    new_msg = TestMessage.from_json(json_str)
    assert new_msg == msg


def test_cross_reference() -> None:
    from otel_test_json.trace.v1.trace import Span  # type: ignore
    from otel_test_json.common.v1.common import InstrumentationScope  # type: ignore

    span = Span(
        name="my-span",
        scope=InstrumentationScope(name="my-scope", version="1.0.0"),
    )

    json_str = span.to_json()
    data = json.loads(json_str)

    assert data["name"] == "my-span"
    assert data["scope"]["name"] == "my-scope"
    assert data["scope"]["version"] == "1.0.0"

    new_span = Span.from_json(json_str)
    assert new_span == span


def test_special_floats() -> None:
    from otel_test_json.test.v1.test import TestMessage  # type: ignore
    import math

    msg = TestMessage(double_value=float("nan"))
    json_str = msg.to_json()
    assert '"doubleValue": "NaN"' in json_str

    new_msg = TestMessage.from_json(json_str)
    assert math.isnan(new_msg.double_value)


def test_defaults() -> None:
    from otel_test_json.test.v1.test import TestMessage  # type: ignore

    msg = TestMessage()
    assert msg.to_json() == "{}"


def test_validation() -> None:
    from otel_test_json.test.v1.test import TestMessage  # type: ignore

    with pytest.raises(TypeError):
        TestMessage.from_dict({"intValue": "not an int"})  # type: ignore
