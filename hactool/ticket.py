import enum
from .abstract import AbstractForInput

class Ticket(AbstractForInput):
    """
    For format specification see https://switchbrew.org/wiki/Ticket
    """

    class SignatureType(enum.Enum):
        RSA_4096_SHA1 = 0x10000
        RSA_2048_SHA1 = 0x10001
        ECDSA_SHA1 = 0x10002
        RSA_4096_SHA256 = 0x10003
        RSA_2048_SHA256 = 0x10004
        ECDSA_SHA256 = 0x10005

    # Signature type: (signature size, padding size)
    sig_info = {
        SignatureType.RSA_4096_SHA1: (0x200, 0x3c),
        SignatureType.RSA_2048_SHA1: (0x100, 0x3c),
        SignatureType.ECDSA_SHA1: (0x3c, 0x40),
        SignatureType.RSA_4096_SHA256: (0x100, 0x3c),
        SignatureType.RSA_2048_SHA256: (0x100, 0x3c),
        SignatureType.ECDSA_SHA256: (0x3c, 0x40)
    }

    def __init__(self, input):
        super().__init__(input)

        self.sig_type = self.SignatureType(self.read_fmt("I"))

        sig_info = self.sig_info[self.sig_type]
        self.sig = self.read_fmt(f"{sig_info[0]}s{sig_info[1]}x")
        self.seek(self.tell() % 0x40, 1)

        self.issuer = self.read(0x40).split(b"\x00", 1)[0].decode()

        self.title_key = self.read_fmt(f"{0x10}s{0xf1}x")

        self.title_key_type = self.read_fmt(f"B{0x3}x")

        self.master_key_rev = self.read_fmt(f"B{0xA}x")

        self.ticket_id, self.device_id = self.read_fmt("QQ")

        self.rights_id = (self.read_fmt("Q", endian=">") << 64) | self.read_fmt("Q", endian=">")

        self.account_id = self.read_fmt("I")