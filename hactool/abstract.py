import io
import struct
from pathlib import Path
from . import util

class AbstractForInput(io.IOBase):
    """
    Helper class for reading data from a file or a buffer
    """

    def __init__(self, input):
        if isinstance(input, str) or isinstance(input, Path):
            self.input = open(input, "rb")
        elif isinstance(input, io.IOBase):
            self.input = input
        else:
            self.input = io.BytesIO(input)

    def seek(self, pos, whence=0):
        return self.input.seek(pos, whence)

    def read(self, size=-1):
        return self.input.read(size)

    def read_fmt(self, fmt, *, endian="<"):
        return util.read_fmt(fmt, self.input, self.tell(), endian=endian)

    def __enter__(self):
        return self

    def close(self):
        self.input.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()