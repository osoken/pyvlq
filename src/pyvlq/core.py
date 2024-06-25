from io import BytesIO


def encode(value: int) -> bytes:
    """Encode a value into a VLQ byte sequence.

    Encode a value into a VLQ byte sequence.

    Args:
        value: The value to encode.

    Returns:
        The VLQ byte sequence.

    Raises:
        ValueError: If the value is negative.

    >>> encode(0)
    b'\\x00'
    >>> encode(1)
    b'\\x01'
    >>> encode(128)
    b'\\x81\\x00'
    >>> encode(268435456)
    b'\\x81\\x80\\x80\\x80\\x00'
    >>> encode(-1)
    Traceback (most recent call last):
     ...
    ValueError: Value must be non-negative
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if value == 0:
        return b"\x00"
    result = bytearray()
    while value:
        byte = value & 0x7F
        value >>= 7
        result.append(byte | 0x80)
    result.reverse()
    result[-1] &= 0x7F
    return bytes(result)


def decode(data: bytes) -> int:
    """Decode a VLQ byte sequence into a value.

    Decode a VLQ byte sequence into a value.

    Args:
        data: The VLQ byte sequence.

    Returns:
        The decoded value.

    Raises:
        ValueError: If the byte sequence is malformed.

    >>> decode(b'\\x00')
    0
    >>> decode(b'\\x01')
    1
    >>> decode(b'\\x7f')
    127
    >>> decode(b'\\x81\\x80\\x80\\x80\\x00')
    268435456
    >>> decode(b'\\x81\\x80')
    Traceback (most recent call last):
     ...
    ValueError: Malformed VLQ byte sequence
    """
    value = 0
    for byte in data:
        value <<= 7
        value |= byte & 0x7F
        if not byte & 0x80:
            return value
    raise ValueError("Malformed VLQ byte sequence")


def decode_stream(data: BytesIO) -> int:
    """Decode a VLQ byte sequence into a value.

    Decode a VLQ byte sequence from a stream.
    This function reads from a stream. It consumes the stream up to the end of the VLQ byte sequence.
    This function is useful when the byte sequence is part of a larger stream.

    Args:
        data: The VLQ byte sequence stream.

    Returns:
        The decoded value.

    Raises:
        ValueError: If the byte sequence is malformed.

    >>> decode_stream(BytesIO(b'\\x00'))
    0
    >>> decode_stream(BytesIO(b'\\x01'))
    1
    >>> decode_stream(BytesIO(b'\\x7f'))
    127
    >>> decode_stream(BytesIO(b'\\x81\\x80\\x80\\x80\\x00'))
    268435456
    >>> buf = BytesIO(b'\\x81\\x80\\x00\\x81\\x80')
    >>> decode_stream(buf)
    16384
    >>> buf.read()
    b'\\x81\\x80'
    >>> decode_stream(BytesIO(b'\\x81\\x80'))
    Traceback (most recent call last):
     ...
    ValueError: Malformed VLQ byte sequence
    """
    value = 0
    while True:
        byte = data.read(1)
        if not byte:
            raise ValueError("Malformed VLQ byte sequence")
        value <<= 7
        value |= byte[0] & 0x7F
        if not byte[0] & 0x80:
            return value
