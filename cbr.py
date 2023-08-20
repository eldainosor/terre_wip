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



    class Frets(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_frets_wave = self._io.read_u4le()
            self.pts_start_wave = self._io.read_u8le()
            self.frets_wave = []
            for i in range(self.num_frets_wave):
                self.frets_wave.append(Cbr.Spark(self._io, self, self._root))



    class Charts(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.diff = self._io.read_u4le()
            self.num_frets_pts = self._io.read_u4le()
            self.time_start = self._io.read_u4le()
            self.pts_frets = []
            for i in range(self.num_frets_pts):
                self.pts_frets.append(self._io.read_u8le())

            self.frets_on_fire = []
            for i in range(self.num_frets_pts):
                self.frets_on_fire.append(Cbr.Frets(self._io, self, self._root))



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
            self.num_waves_pts = self._io.read_u4le()
            self.start_wave_pos = self._io.read_u8le()
            self.num_lyrics_pts = self._io.read_u4le()
            self.start_lyrics_pos = self._io.read_u8le()
            self.lyrics_info = self._io.read_bytes(100)
            self.pts_wave = []
            for i in range(self.num_waves_pts):
                self.pts_wave.append(self._io.read_u8le())

            self.elements = []
            for i in range(self.num_waves_pts):
                self.elements.append(Cbr.Flow(self._io, self, self._root))

            self.pts_lyrics = []
            for i in range(self.num_lyrics_pts):
                self.pts_lyrics.append(self._io.read_u8le())

            self.lyrics = []
            for i in range(self.num_lyrics_pts):
                self.lyrics.append(Cbr.Verse(self._io, self, self._root))



    class Syllable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.time_start = self._io.read_u4le()
            self.time_end = self._io.read_u4le()
            self.type = self._io.read_u4le()
            self.text = (self._io.read_bytes_term(0, False, True, True)).decode(u"WINDOWS-1252")


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
                self.song.append(Cbr.Notes(self._io, self, self._root))
                i += 1



    class Spark(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.fire = []
            for i in range(3):
                self.fire.append(self._io.read_u4le())



    class Flow(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x02\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x02\x00\x00\x00", self.magic, self._io, u"/types/flow/seq/0")
            self.next_pt = self._io.read_u8le()
            self.water = []
            for i in range(8):
                self.water.append(self._io.read_u4le())



    class Verse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_text = self._io.read_u4le()
            self.info = []
            for i in range(6):
                self.info.append(self._io.read_u4le())

            self.pts_text = []
            for i in range(self.num_text):
                self.pts_text.append(self._io.read_u8le())

            self.text_block = []
            for i in range(self.num_text):
                self.text_block.append(Cbr.Syllable(self._io, self, self._root))



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.instrument_id = KaitaiStream.resolve_enum(Cbr.InstId, self._io.read_u4le())
            self.channel = self._io.read_u4le()
            self.start_diff_pos = self._io.read_u8le()
            self.num_events = self._io.read_u4le()
            self.start_events_pos = self._io.read_u8le()
            self.bpm = KaitaiStream.bytes_terminate(self._io.read_bytes(484), 0, False)
            self.events = []
            for i in range(self.num_events):
                self.events.append(Cbr.Event(self._io, self, self._root))



    class Notes(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()
            self.bar = self._io.read_u2le()


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

            self.easy = Cbr.Charts(self._io, self, self._root)
            self.norm = Cbr.Charts(self._io, self, self._root)
            self.hard = Cbr.Charts(self._io, self, self._root)



