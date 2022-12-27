# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cbr(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Cbr.Header(self._io, self, self._root)
        self.song_name = Cbr.SongName(self._io, self, self._root)
        self.charts = Cbr.Charts(self._io, self, self._root)

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x76\x98\xCD\xAB":
                raise kaitaistruct.ValidationNotEqualError(b"\x76\x98\xCD\xAB", self.magic, self._io, u"/types/header/seq/0")
            self.flags_1 = self._io.read_u8le()
            self.song_id = self._io.read_u8le()
            self.flags_2 = self._io.read_u8le()
            self.band_id = self._io.read_u8le()
            self.disc_id = self._io.read_u8le()
            self.year = self._io.read_u4le()


    class SongName(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.song_name = (self._io.read_bytes(256)).decode(u"UTF-16")


    class Charts(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(8)
            if not self.magic == b"\x00\x08\x00\x00\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x08\x00\x00\x00\x00\x00\x00", self.magic, self._io, u"/types/charts/seq/0")
            self.pointer = []
            for i in range(4):
                self.pointer.append(self._io.read_u8le())

            self.data = []
            for i in range(6):
                self.data.append(self._io.read_u8le())

            self.zeros = self._io.read_bytes(1656)
            self._raw_chart_guitar = self._io.read_bytes((self.pointer[0] - 2048))
            _io__raw_chart_guitar = KaitaiStream(BytesIO(self._raw_chart_guitar))
            self.chart_guitar = Cbr.Instrument(_io__raw_chart_guitar, self, self._root)
            self._raw_chart_rhythm = self._io.read_bytes((self.pointer[1] - self.pointer[0]))
            _io__raw_chart_rhythm = KaitaiStream(BytesIO(self._raw_chart_rhythm))
            self.chart_rhythm = Cbr.Instrument(_io__raw_chart_rhythm, self, self._root)
            self._raw_chart_drums = self._io.read_bytes((self.pointer[2] - self.pointer[1]))
            _io__raw_chart_drums = KaitaiStream(BytesIO(self._raw_chart_drums))
            self.chart_drums = Cbr.Instrument(_io__raw_chart_drums, self, self._root)
            self._raw_chart_vocals = self._io.read_bytes((self.pointer[3] - self.pointer[2]))
            _io__raw_chart_vocals = KaitaiStream(BytesIO(self._raw_chart_vocals))
            self.chart_vocals = Cbr.Instrument(_io__raw_chart_vocals, self, self._root)
            self.chart_ending = Cbr.Instrument(self._io, self, self._root)


    class Instrument(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.intro = []
            for i in range(4):
                self.intro.append(self._io.read_u8le())

            self.zeros = self._io.read_bytes(480)
            self.head = []
            for i in range(873):
                self.head.append(self._io.read_u8le())

            self.raw = self._io.read_bytes_full()



