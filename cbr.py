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

    class Body(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.val = self._io.read_u2le()
            self.len = self._io.read_u2le()
            self.num = self._io.read_u4le()


    class Frets(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.notes = self._io.read_u4le()


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
            self._raw_guitar = self._io.read_bytes((self.pointer[0] - 2048))
            _io__raw_guitar = KaitaiStream(BytesIO(self._raw_guitar))
            self.guitar = Cbr.Instrument(_io__raw_guitar, self, self._root)
            self._raw_rhythm = self._io.read_bytes((self.pointer[1] - self.pointer[0]))
            _io__raw_rhythm = KaitaiStream(BytesIO(self._raw_rhythm))
            self.rhythm = Cbr.Instrument(_io__raw_rhythm, self, self._root)
            self._raw_drums = self._io.read_bytes((self.pointer[2] - self.pointer[1]))
            _io__raw_drums = KaitaiStream(BytesIO(self._raw_drums))
            self.drums = Cbr.Instrument(_io__raw_drums, self, self._root)
            if self.pointer[3] != 0:
                self._raw_voice = self._io.read_bytes((self.pointer[3] - self.pointer[2]))
                _io__raw_voice = KaitaiStream(BytesIO(self._raw_voice))
                self.voice = Cbr.Voice(_io__raw_voice, self, self._root)

            if self.pointer[3] != 0:
                self._raw_extras = self._io.read_bytes_full()
                _io__raw_extras = KaitaiStream(BytesIO(self._raw_extras))
                self.extras = Cbr.Separator(_io__raw_extras, self, self._root)

            if self.pointer[3] == 0:
                self._raw_voice2 = self._io.read_bytes_full()
                _io__raw_voice2 = KaitaiStream(BytesIO(self._raw_voice2))
                self.voice2 = Cbr.Voice(_io__raw_voice2, self, self._root)



    class Separator(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_bytes(8)
            self.end_pos = self._io.read_u8le()
            self.size_bytes = self._io.read_u4le()
            self.start_pos = self._io.read_u8le()
            self.fill = self._io.read_u4le()
            self.zeros = self._io.read_bytes(480)
            self.head = []
            for i in range(self.size_bytes):
                self.head.append(Cbr.Body(self._io, self, self._root))



    class Voice(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = Cbr.Separator(self._io, self, self._root)
            self.info = self._io.read_bytes(8)
            self.start_pitch_pos = self._io.read_u8le()
            self.pitch_vol = self._io.read_u4le()
            self.start_lyrics_pos = self._io.read_u8le()
            self.lyrics_vol = self._io.read_u4le()
            self.zeros = self._io.read_bytes(96)
            self._raw_pitch_pts = self._io.read_bytes((self.start_lyrics_pos - self.start_pitch_pos))
            _io__raw_pitch_pts = KaitaiStream(BytesIO(self._raw_pitch_pts))
            self.pitch_pts = Cbr.Array(_io__raw_pitch_pts, self, self._root)
            self.lyrics = self._io.read_bytes_full()


    class Array(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.song = []
            i = 0
            while not self._io.is_eof():
                self.song.append(self._io.read_u4le())
                i += 1



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
            self.header = Cbr.Separator(self._io, self, self._root)
            self.info = self._io.read_bytes(8)
            self.diff_point = []
            for i in range(3):
                self.diff_point.append(self._io.read_u8le())

            self.zeros = self._io.read_bytes(96)
            self._raw_easy = self._io.read_bytes((self.diff_point[1] - self.diff_point[0]))
            _io__raw_easy = KaitaiStream(BytesIO(self._raw_easy))
            self.easy = Cbr.Array(_io__raw_easy, self, self._root)
            self._raw_norm = self._io.read_bytes((self.diff_point[2] - self.diff_point[1]))
            _io__raw_norm = KaitaiStream(BytesIO(self._raw_norm))
            self.norm = Cbr.Array(_io__raw_norm, self, self._root)
            self._raw_hard = self._io.read_bytes_full()
            _io__raw_hard = KaitaiStream(BytesIO(self._raw_hard))
            self.hard = Cbr.Array(_io__raw_hard, self, self._root)



