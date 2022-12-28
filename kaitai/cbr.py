# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cbr(KaitaiStruct):

    class InstId(Enum):
        guitar = 0
        rhythm = 1
        drums = 2
        voice = 3
        song = 4
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Cbr.Header(self._io, self, self._root)
        self.charts = Cbr.Charts(self._io, self, self._root)

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

            self.info = []
            for i in range(12):
                self.info.append(self._io.read_bytes(4))

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
            self._raw_chart_voice = self._io.read_bytes((self.pointer[3] - self.pointer[2]))
            _io__raw_chart_voice = KaitaiStream(BytesIO(self._raw_chart_voice))
            self.chart_voice = Cbr.Voice(_io__raw_chart_voice, self, self._root)
            self._raw_end_of_charts = self._io.read_bytes_full()
            _io__raw_end_of_charts = KaitaiStream(BytesIO(self._raw_end_of_charts))
            self.end_of_charts = Cbr.ChartHead(_io__raw_end_of_charts, self, self._root)


    class Voice(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = Cbr.ChartHead(self._io, self, self._root)
            self.info = self._io.read_bytes(8)
            self.start_pitch_pos = self._io.read_u8le()
            self.pitch_vol = self._io.read_u4le()
            self.start_lyrics_pos = self._io.read_u8le()
            self.lyrics_vol = self._io.read_u4le()
            self.zeros = self._io.read_bytes(96)
            self.pitch = self._io.read_bytes((self.start_lyrics_pos - self.start_pitch_pos))
            self.lyrics = self._io.read_bytes_full()


    class ChartHead(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_bytes(8)
            self.end_head_pos = self._io.read_u8le()
            self.size_head_bytes = self._io.read_u4le()
            self.start_head_pos = self._io.read_u8le()
            self.size_zero_fill = self._io.read_u4le()
            self.zeros = self._io.read_bytes(480)
            self.head = self._io.read_bytes((self.size_head_bytes * 8))


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
            self.flags_1 = self._io.read_bytes(8)
            self.song_id = self._io.read_u8le()
            self.flags_2 = self._io.read_bytes(8)
            self.band_id = self._io.read_u8le()
            self.disc_id = self._io.read_u8le()
            self.year = self._io.read_u4le()
            self.song_name = (self._io.read_bytes(256)).decode(u"UTF-16")


    class Instrument(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = Cbr.ChartHead(self._io, self, self._root)
            self.info = self._io.read_bytes(8)
            self.diff_point = []
            for i in range(3):
                self.diff_point.append(self._io.read_u8le())

            self.zeros = self._io.read_bytes(96)
            self.chart_easy = self._io.read_bytes((self.diff_point[1] - self.diff_point[0]))
            self.chart_med = self._io.read_bytes((self.diff_point[2] - self.diff_point[1]))
            self.chart_hard = self._io.read_bytes_full()



