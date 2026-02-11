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

# AUTO-GENERATED from "otel_test_json/test/v1/test.proto"
# DO NOT EDIT MANUALLY

from __future__ import annotations

import builtins
import dataclasses
import enum
import functools
import json
import sys
import typing

if sys.version_info >= (3, 10):
    _dataclass = functools.partial(dataclasses.dataclass, slots=True)
else:
    _dataclass = dataclasses.dataclass

import otel_test_json._otlp_json_utils as _utils


@typing.final
@_dataclass
class TestMessage:
    """
    Generated from protobuf message TestMessage
    """

    @typing.final
    class TestEnum(enum.IntEnum):
        """
        Generated from protobuf enum TestEnum
        """

        UNSPECIFIED = 0
        SUCCESS = 1
        FAILURE = 2

    name: typing.Optional[builtins.str] = ""
    int_value: typing.Optional[builtins.int] = 0
    bool_value: typing.Optional[builtins.bool] = False
    double_value: typing.Optional[builtins.float] = 0.0
    int64_value: typing.Optional[builtins.int] = 0
    uint64_value: typing.Optional[builtins.int] = 0
    bytes_value: typing.Optional[builtins.bytes] = b""
    trace_id: typing.Optional[builtins.bytes] = b""
    span_id: typing.Optional[builtins.bytes] = b""
    list_strings: builtins.list[builtins.str] = dataclasses.field(default_factory=builtins.list)
    list_ints: builtins.list[builtins.int] = dataclasses.field(default_factory=builtins.list)
    enum_value: typing.Union[TestMessage.TestEnum, builtins.int, None] = 0
    sub_message: typing.Optional[SubMessage] = None
    list_messages: builtins.list[SubMessage] = dataclasses.field(default_factory=builtins.list)
    oneof_string: typing.Optional[builtins.str] = None
    oneof_int: typing.Optional[builtins.int] = None

    def to_dict(self) -> builtins.dict[builtins.str, typing.Any]:
        """
        Convert this message to a dictionary with lowerCamelCase keys.

        Returns:
            Dictionary representation following OTLP JSON encoding
        """
        _result = {}
        if self.name:
            _result["name"] = self.name
        if self.int_value:
            _result["intValue"] = self.int_value
        if self.bool_value:
            _result["boolValue"] = self.bool_value
        if self.double_value:
            _result["doubleValue"] = _utils.encode_float(self.double_value)
        if self.int64_value:
            _result["int64Value"] = _utils.encode_int64(self.int64_value)
        if self.uint64_value:
            _result["uint64Value"] = _utils.encode_int64(self.uint64_value)
        if self.bytes_value:
            _result["bytesValue"] = _utils.encode_base64(self.bytes_value)
        if self.trace_id:
            _result["traceId"] = _utils.encode_hex(self.trace_id)
        if self.span_id:
            _result["spanId"] = _utils.encode_hex(self.span_id)
        if self.list_strings:
            _result["listStrings"] = self.list_strings
        if self.list_ints:
            _result["listInts"] = self.list_ints
        if self.enum_value:
            _result["enumValue"] = builtins.int(self.enum_value)
        if self.sub_message:
            _result["subMessage"] = self.sub_message.to_dict()
        if self.list_messages:
            _result["listMessages"] = _utils.encode_repeated(self.list_messages, lambda _v: _v.to_dict())
        if self.oneof_int is not None:
            _result["oneofInt"] = self.oneof_int
        elif self.oneof_string is not None:
            _result["oneofString"] = self.oneof_string
        return _result

    def to_json(self) -> builtins.str:
        """
        Serialize this message to a JSON string.

        Returns:
            JSON string
        """
        return json.dumps(self.to_dict())

    @builtins.classmethod
    def from_dict(cls, data: builtins.dict[builtins.str, typing.Any]) -> "TestMessage":
        """
        Create from a dictionary with lowerCamelCase keys.

        Args:
            data: Dictionary representation following OTLP JSON encoding

        Returns:
            TestMessage instance
        """
        _utils.validate_type(data, builtins.dict, "data")
        _args = {}

        if (_value := data.get("name")) is not None:
            _utils.validate_type(_value, builtins.str, "name")
            _args["name"] = _value
        if (_value := data.get("intValue")) is not None:
            _utils.validate_type(_value, builtins.int, "int_value")
            _args["int_value"] = _value
        if (_value := data.get("boolValue")) is not None:
            _utils.validate_type(_value, builtins.bool, "bool_value")
            _args["bool_value"] = _value
        if (_value := data.get("doubleValue")) is not None:
            _args["double_value"] = _utils.decode_float(_value, "double_value")
        if (_value := data.get("int64Value")) is not None:
            _args["int64_value"] = _utils.decode_int64(_value, "int64_value")
        if (_value := data.get("uint64Value")) is not None:
            _args["uint64_value"] = _utils.decode_int64(_value, "uint64_value")
        if (_value := data.get("bytesValue")) is not None:
            _args["bytes_value"] = _utils.decode_base64(_value, "bytes_value")
        if (_value := data.get("traceId")) is not None:
            _args["trace_id"] = _utils.decode_hex(_value, "trace_id")
        if (_value := data.get("spanId")) is not None:
            _args["span_id"] = _utils.decode_hex(_value, "span_id")
        if (_value := data.get("listStrings")) is not None:
            _args["list_strings"] = _utils.decode_repeated(_value, lambda _v: _v, "list_strings")
        if (_value := data.get("listInts")) is not None:
            _args["list_ints"] = _utils.decode_repeated(_value, lambda _v: _v, "list_ints")
        if (_value := data.get("enumValue")) is not None:
            _utils.validate_type(_value, builtins.int, "enum_value")
            _args["enum_value"] = TestMessage.TestEnum(_value)
        if (_value := data.get("subMessage")) is not None:
            _args["sub_message"] = SubMessage.from_dict(_value)
        if (_value := data.get("listMessages")) is not None:
            _args["list_messages"] = _utils.decode_repeated(_value, lambda _v: SubMessage.from_dict(_v), "list_messages")
        if (_value := data.get("oneofInt")) is not None:
            _utils.validate_type(_value, builtins.int, "oneof_int")
            _args["oneof_int"] = _value
        elif (_value := data.get("oneofString")) is not None:
            _utils.validate_type(_value, builtins.str, "oneof_string")
            _args["oneof_string"] = _value

        return cls(**_args)

    @builtins.classmethod
    def from_json(cls, data: typing.Union[builtins.str, builtins.bytes]) -> "TestMessage":
        """
        Deserialize from a JSON string or bytes.

        Args:
            data: JSON string or bytes

        Returns:
            Instance of the class
        """
        return cls.from_dict(json.loads(data))


@typing.final
@_dataclass
class SubMessage:
    """
    Generated from protobuf message SubMessage
    """

    content: typing.Optional[builtins.str] = ""

    def to_dict(self) -> builtins.dict[builtins.str, typing.Any]:
        """
        Convert this message to a dictionary with lowerCamelCase keys.

        Returns:
            Dictionary representation following OTLP JSON encoding
        """
        _result = {}
        if self.content:
            _result["content"] = self.content
        return _result

    def to_json(self) -> builtins.str:
        """
        Serialize this message to a JSON string.

        Returns:
            JSON string
        """
        return json.dumps(self.to_dict())

    @builtins.classmethod
    def from_dict(cls, data: builtins.dict[builtins.str, typing.Any]) -> "SubMessage":
        """
        Create from a dictionary with lowerCamelCase keys.

        Args:
            data: Dictionary representation following OTLP JSON encoding

        Returns:
            SubMessage instance
        """
        _utils.validate_type(data, builtins.dict, "data")
        _args = {}

        if (_value := data.get("content")) is not None:
            _utils.validate_type(_value, builtins.str, "content")
            _args["content"] = _value

        return cls(**_args)

    @builtins.classmethod
    def from_json(cls, data: typing.Union[builtins.str, builtins.bytes]) -> "SubMessage":
        """
        Deserialize from a JSON string or bytes.

        Args:
            data: JSON string or bytes

        Returns:
            Instance of the class
        """
        return cls.from_dict(json.loads(data))
