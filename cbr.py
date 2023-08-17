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

    class Lister(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pointers = []
            i = 0
            while not self._io.is_eof():
                self.pointers.append(self._io.read_u8le())
                i += 1



    class Event(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()
            self.type = self._io.read_u4le()


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
            for i in range(5):
                self.trk_pts.append(self._io.read_u8le())

            self.diff_level = []
            for i in range(6):
                self.diff_level.append(self._io.read_u2le())

            self.trk_info = []
            for i in range(6):
                self.trk_info.append(self._io.read_u4le())

            self.trk_vol = KaitaiStream.bytes_terminate(self._io.read_bytes(1660), 0, False)
            if self.trk_pts[0] != 0:
                self._raw_guitar = self._io.read_bytes((self.trk_pts[0] - 2048))
                _io__raw_guitar = KaitaiStream(BytesIO(self._raw_guitar))
                self.guitar = Cbr.Instrument(_io__raw_guitar, self, self._root)

            if self.trk_pts[1] != 0:
                self._raw_rhythm = self._io.read_bytes((self.trk_pts[1] - self.trk_pts[0]))
                _io__raw_rhythm = KaitaiStream(BytesIO(self._raw_rhythm))
                self.rhythm = Cbr.Instrument(_io__raw_rhythm, self, self._root)

            if self.trk_pts[2] != 0:
                self._raw_drums = self._io.read_bytes((self.trk_pts[2] - self.trk_pts[1]))
                _io__raw_drums = KaitaiStream(BytesIO(self._raw_drums))
                self.drums = Cbr.Instrument(_io__raw_drums, self, self._root)

            if self.trk_pts[3] != 0:
                self._raw_vocals_with_extras = self._io.read_bytes((self.trk_pts[3] - self.trk_pts[2]))
                _io__raw_vocals_with_extras = KaitaiStream(BytesIO(self._raw_vocals_with_extras))
                self.vocals_with_extras = Cbr.Voice(_io__raw_vocals_with_extras, self, self._root)

            if self.trk_pts[3] != 0:
                self.extras = Cbr.Header(self._io, self, self._root)

            if self.trk_pts[3] == 0:
                self._raw_vocals_no_extras = self._io.read_bytes_full()
                _io__raw_vocals_no_extras = KaitaiStream(BytesIO(self._raw_vocals_no_extras))
                self.vocals_no_extras = Cbr.Voice(_io__raw_vocals_no_extras, self, self._root)



    class Voice(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hdr = Cbr.Header(self._io, self, self._root)
            self.magic1 = self._io.read_bytes(4)
            if not self.magic1 == b"\x05\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x05\x00\x00\x00", self.magic1, self._io, u"/types/voice/seq/1")
            self.info = self._io.read_u4le()
            self.start_wave_pos = self._io.read_u8le()
            self.wave_vol = self._io.read_u4le()
            self.start_lyrics_pos = self._io.read_u8le()
            self.lyrics_vol = KaitaiStream.bytes_terminate(self._io.read_bytes(100), 0, False)
            self._raw_pts_frets = self._io.read_bytes((self.info * 8))
            _io__raw_pts_frets = KaitaiStream(BytesIO(self._raw_pts_frets))
            self.pts_frets = Cbr.Lister(_io__raw_pts_frets, self, self._root)
            self.magic2 = self._io.read_bytes(4)
            if not self.magic2 == b"\x02\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x02\x00\x00\x00", self.magic2, self._io, u"/types/voice/seq/8")
            self._raw_norm = self._io.read_bytes((((self.start_lyrics_pos - self.start_wave_pos) - (self.info * 8)) - 4))
            _io__raw_norm = KaitaiStream(BytesIO(self._raw_norm))
            self.norm = Cbr.Array(_io__raw_norm, self, self._root)
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



    class Verse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.start = self._io.read_u2le()
            self.line_in = self._io.read_u2le()
            self.end = self._io.read_u2le()
            self.line_out = self._io.read_u2le()
            self.verse_type2 = self._io.read_u2le()
            self.verse_type3 = self._io.read_u2le()
            if self.start < self.end:
                self.text = (self._io.read_bytes_term(0, False, True, True)).decode(u"ASCII")



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.instrument_id = KaitaiStream.resolve_enum(Cbr.InstId, self._io.read_u4le())
            self.channel = self._io.read_u4le()
            self.end_pos = self._io.read_u8le()
            self.size_bytes = self._io.read_u4le()
            self.start_pos = self._io.read_u8le()
            self.bpm = KaitaiStream.bytes_terminate(self._io.read_bytes(484), 0, False)
            self.events = []
            for i in range(self.size_bytes):
                self.events.append(Cbr.Event(self._io, self, self._root))



    class Notes(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u1()
            self.bar = self._io.read_u1()
            self.pos = self._io.read_u2le()


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
            self.hdr = Cbr.Header(self._io, self, self._root)
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



