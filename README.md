# pyvlq
pyvlq is a Python library for encoding and decoding `Variable-Length Quantity <https://en.wikipedia.org/wiki/Variable-length_quantity>`_.

The library is available on PyPI and can be installed using pip:

```bash
pip install pyvlq
```

## Usage
```python
from io import BytesIO
import pyvlq

# Encode
encoded = pyvlq.encode(128)
print(encoded) # b'\x81\x00'

# Decode
decoded = pyvlq.decode(encoded)
print(decoded) # 128

# Decode from readable bytes
buffer = BytesIO(b'\x81\x00\xff\xff')
decoded = pyvlq.decode_stream(buffer)
print(decoded) # 128 (0xff\xff is ignored)
print(buffer.read(2)) # b'\xff\xff' (0xff\xff is left in the buffer)
```
