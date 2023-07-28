# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Disc(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Disc.Header(self._io, self, self._root)
        self.disc_name = (self._io.read_bytes(256)).decode(u"UTF-16")
        self.image = Disc.Image(self._io, self, self._root)

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x00\x00\xCC\xD1":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\xCC\xD1", self.magic, self._io, u"/types/header/seq/0")
            self.version = self._io.read_u4le()
            self.disc_id = self._io.read_u8le()
            self.band_id = self._io.read_u8le()


    class Image(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(8)
            if not self.magic == b"\x00\x08\x00\x00\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x08\x00\x00\x00\x00\x00\x00", self.magic, self._io, u"/types/image/seq/0")
            self.img_size = self._io.read_u4le()
            self.year = self._io.read_u4le()
            self.spacer = self._io.read_bytes(1752)
            self.png = self._io.read_bytes(self.img_size)



