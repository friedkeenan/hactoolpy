import io
from .abstract import AbstractForInput

class PFS0(AbstractForInput):
    """
    For format specification, see https://switchbrew.org/wiki/NCA_Format#PFS0
    """

    magic = b"PFS0"

    class FileEntry(io.IOBase):
        def __init__(self, pfs0, offset=None):
            super().__init__()

            self.pfs0 = pfs0

            if offset is not None:
                pfso.seek(offset)

            self.data_off, self.data_size = pfs0.read_fmt("QQ")
            self.name_off = pfs0.read_fmt(f"I{0x4}x")

            self.name = None
            self.curr_off = 0

        def seek(self, pos, whence=0):
            if whence == 0:
                self.curr_off = pos
            elif whence == 1:
                self.curr_off += pos
            elif whence == 2:
                self.curr_off = self.data_size + pos
            else:
                raise ValueError("Invalid whence argument")

            return self.curr_off

        def read(self, size=-1):
            self.pfs0.seek(self.pfs0.header_size + self.data_off + self.curr_off)

            if size < 0:
                size = self.data_size

            ret = self.pfs0.read(size)
            self.seek(size, 1)

            return ret

        def read_chunks(self, chunk_size, length=None):
            self.pfs0.seek(self.pfs0.header_size + self.data_off)

            if length is None:
                length = self.data_size

            to_read = length

            while to_read > 0:
                curr_read = min(chunk_size, to_read)
                yield self.pfs0.read_fmt(f"{curr_read}s")

                self.seek(curr_read, 1)
                to_read -= curr_read

        def __repr__(self):
            return f'{type(self)}(name="{self.name}")'

    def __init__(self, input):
        super().__init__(input)

        if self.read_fmt(f"{len(self.magic)}s") != self.magic:
            raise ValueError("Invalid PFS0 magic")

        num_files, str_table_size = self.read_fmt(f"II{0x4}x")

        self.files = [self.FileEntry(self) for x in range(num_files)]

        str_table = self.read_fmt(f"{str_table_size}s")
        str_table = str_table.split(b"\x00", num_files)

        self.header_size = self.tell()

        for i in range(num_files):
            self.files[i].name = str_table[i].decode()