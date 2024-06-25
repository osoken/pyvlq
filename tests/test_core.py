from io import BytesIO

import pytest

from pyvlq.core import decode, decode_stream, encode


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        (0, b"\x00"),
        (1, b"\x01"),
        (127, b"\x7f"),
        (128, b"\x81\x00"),
        (129, b"\x81\x01"),
        (8192, b"\xc0\x00"),
        (16383, b"\xff\x7f"),
        (16384, b"\x81\x80\x00"),
        (16385, b"\x81\x80\x01"),
        (2097151, b"\xff\xff\x7f"),
        (2097152, b"\x81\x80\x80\x00"),
        (2097153, b"\x81\x80\x80\x01"),
        (268435455, b"\xff\xff\xff\x7f"),
        (268435456, b"\x81\x80\x80\x80\x00"),
    ],
)
def test_encode(input: int, expected: bytes) -> None:
    assert encode(input) == expected


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        (b"\x00", 0),
        (b"\x01", 1),
        (b"\x7f", 127),
        (b"\x81\x00", 128),
        (b"\x81\x01", 129),
        (b"\xc0\x00", 8192),
        (b"\xff\x7f", 16383),
        (b"\x81\x80\x00", 16384),
        (b"\x81\x80\x01", 16385),
        (b"\xff\xff\x7f", 2097151),
        (b"\x81\x80\x80\x00", 2097152),
        (b"\x81\x80\x80\x01", 2097153),
        (b"\xff\xff\xff\x7f", 268435455),
        (b"\x81\x80\x80\x80\x00", 268435456),
    ],
)
def test_decode(input: bytes, expected: int) -> None:
    assert decode(input) == expected


@pytest.mark.parametrize(
    "input",
    [
        b"\x80",
        b"\x80\x80",
        b"\x80\x80\x80",
        b"\x80\x80\x80\x80",
        b"\x80\x80\x80\x80\x80",
    ],
)
def test_decode_malformed(input: bytes) -> None:
    with pytest.raises(ValueError):
        decode(input)


def test_encode_negative() -> None:
    with pytest.raises(ValueError):
        encode(-1)


@pytest.mark.parametrize(
    ("input", "expected", "remainder"),
    [
        (b"\x00", 0, b""),
        (b"\x01", 1, b""),
        (b"\x7f", 127, b""),
        (b"\x01\x00", 1, b"\x00"),
        (b"\x00\x01", 0, b"\x01"),
        (b"\x81\x80\x80\x80\x00\x42\x23\x00\x21", 268435456, b"\x42\x23\x00\x21"),
    ],
)
def test_decode_partial(input: bytes, expected: int, remainder: bytes) -> None:
    buffer = BytesIO(input)
    assert decode_stream(buffer) == expected
    assert buffer.read() == remainder


def test_decode_stream_malformed() -> None:
    with pytest.raises(ValueError):
        decode_stream(BytesIO(b"\x80"))
