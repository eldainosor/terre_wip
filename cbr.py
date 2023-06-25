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
        self.info = Cbr.MetaData(self._io, self, self._root)
        self.tracks = Cbr.Track(self._io, self, self._root)

    class Frets(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.fret = self._io.read_bytes(4)


    class Event(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.val = self._io.read_bytes(8)


    class Separator(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.channel = self._io.read_u8le()
            self.end_pos = self._io.read_u8le()
            self.size_bytes = self._io.read_u4le()
            self.start_pos = self._io.read_u8le()
            self.bpm = self._io.read_u4le()
            self.zeros60 = []
            for i in range(60):
                self.zeros60.append(self._io.read_u8le())

            self.events = []
            for i in range(self.size_bytes):
                self.events.append(Cbr.Event(self._io, self, self._root))



    class Track(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(8)
            if not self.magic == b"\x00\x08\x00\x00\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x08\x00\x00\x00\x00\x00\x00", self.magic, self._io, u"/types/track/seq/0")
            self.trk_pts = []
            for i in range(217):
                self.trk_pts.append(self._io.read_u8le())

            self._raw_guitar = self._io.read_bytes((self.trk_pts[0] - 2048))
            _io__raw_guitar = KaitaiStream(BytesIO(self._raw_guitar))
            self.guitar = Cbr.Instrument(_io__raw_guitar, self, self._root)
            self._raw_rhythm = self._io.read_bytes((self.trk_pts[1] - self.trk_pts[0]))
            _io__raw_rhythm = KaitaiStream(BytesIO(self._raw_rhythm))
            self.rhythm = Cbr.Instrument(_io__raw_rhythm, self, self._root)
            self._raw_drums = self._io.read_bytes((self.trk_pts[2] - self.trk_pts[1]))
            _io__raw_drums = KaitaiStream(BytesIO(self._raw_drums))
            self.drums = Cbr.Instrument(_io__raw_drums, self, self._root)
            if self.trk_pts[3] != 0:
                self._raw_voice = self._io.read_bytes((self.trk_pts[3] - self.trk_pts[2]))
                _io__raw_voice = KaitaiStream(BytesIO(self._raw_voice))
                self.voice = Cbr.Voice(_io__raw_voice, self, self._root)

            if self.trk_pts[3] != 0:
                self._raw_extras = self._io.read_bytes_full()
                _io__raw_extras = KaitaiStream(BytesIO(self._raw_extras))
                self.extras = Cbr.Separator(_io__raw_extras, self, self._root)

            if self.trk_pts[3] == 0:
                self._raw_voice2 = self._io.read_bytes_full()
                _io__raw_voice2 = KaitaiStream(BytesIO(self._raw_voice2))
                self.voice2 = Cbr.Voice(_io__raw_voice2, self, self._root)



    class Voice(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = Cbr.Separator(self._io, self, self._root)
            self.info = self._io.read_u8le()
            self.start_wave_pos = self._io.read_u8le()
            self.wave_vol = self._io.read_u4le()
            self.start_lyrics_pos = self._io.read_u8le()
            self.lyrics_vol = self._io.read_u4le()
            self.zeros12 = []
            for i in range(12):
                self.zeros12.append(self._io.read_u8le())

            self._raw_wave_pts = self._io.read_bytes((self.start_lyrics_pos - self.start_wave_pos))
            _io__raw_wave_pts = KaitaiStream(BytesIO(self._raw_wave_pts))
            self.wave_pts = Cbr.Array(_io__raw_wave_pts, self, self._root)
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
                self.song.append(Cbr.Frets(self._io, self, self._root))
                i += 1



    class MetaData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x76\x98\xCD\xAB":
                raise kaitaistruct.ValidationNotEqualError(b"\x76\x98\xCD\xAB", self.magic, self._io, u"/types/meta_data/seq/0")
            self.flags_1 = self._io.read_u8le()
            self.song_id = self._io.read_u8le()
            self.flags_2 = self._io.read_u8le()
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
            self.magic = self._io.read_bytes(8)
            if not self.magic == b"\x02\x00\x00\x00\x03\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x02\x00\x00\x00\x03\x00\x00\x00", self.magic, self._io, u"/types/instrument/seq/1")
            self.diff_pts = []
            for i in range(15):
                self.diff_pts.append(self._io.read_u8le())

            self._raw_easy = self._io.read_bytes((self.diff_pts[1] - self.diff_pts[0]))
            _io__raw_easy = KaitaiStream(BytesIO(self._raw_easy))
            self.easy = Cbr.Array(_io__raw_easy, self, self._root)
            self._raw_norm = self._io.read_bytes((self.diff_pts[2] - self.diff_pts[1]))
            _io__raw_norm = KaitaiStream(BytesIO(self._raw_norm))
            self.norm = Cbr.Array(_io__raw_norm, self, self._root)
            self._raw_hard = self._io.read_bytes_full()
            _io__raw_hard = KaitaiStream(BytesIO(self._raw_hard))
            self.hard = Cbr.Array(_io__raw_hard, self, self._root)



