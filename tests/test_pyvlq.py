import re

import pyvlq


def test_pyvlq_has_version() -> None:
    assert hasattr(pyvlq, "__version__")
    assert re.match(r"\d+\.\d+\.\d+", pyvlq.__version__)


def test_pyvlq_has_encode() -> None:
    assert hasattr(pyvlq, "encode")
    assert pyvlq.encode == pyvlq.core.encode


def test_pyvlq_has_decode() -> None:
    assert hasattr(pyvlq, "decode")
    assert pyvlq.decode == pyvlq.core.decode


def test_pyvlq_has_decode_stream() -> None:
    assert hasattr(pyvlq, "decode_stream")
    assert pyvlq.decode_stream == pyvlq.core.decode_stream
