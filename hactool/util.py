import struct
import io

def read_fmt(fmt, input, offset=0, *, endian="<"):
    if isinstance(input, io.IOBase): # If input is a file-like object
        input.seek(offset)
        buffer = input.read(struct.calcsize(fmt))
        offset = 0
    else:
        buffer = input

    ret = struct.unpack_from(f"{endian}{fmt}", buffer, offset)

    if len(ret) == 1:
        return ret[0]

    return ret