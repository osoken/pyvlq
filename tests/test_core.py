import pytest

from pyvlq.core import decode, encode


@pytest.mark.parametrize(
    "input, expected",
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
    "input, expected",
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
