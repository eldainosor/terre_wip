# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cbr(KaitaiStruct):

    class DiffLvl(Enum):
        easy = 0
        medium = 1
        hard = 2

    class InstrumId(Enum):
        guitar = 0
        rhythm = 1
        drums = 2
        vocals = 3
        band = 4

    class PosId(Enum):
        lo = 0
        me = 1
        hi = 2

    class ColorId(Enum):
        orange = 0
        blue = 1
        yellow = 2
        red = 3
        green = 4
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic_1 = self._io.read_bytes(4)
        if not self.magic_1 == b"\x76\x98\xCD\xAB":
            raise kaitaistruct.ValidationNotEqualError(b"\x76\x98\xCD\xAB", self.magic_1, self._io, u"/seq/0")
        self.magic_2 = self._io.read_bytes(4)
        if not self.magic_2 == b"\x00\x00\x04\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x04\x00", self.magic_2, self._io, u"/seq/1")
        self.magic_3 = self._io.read_bytes(4)
        if not self.magic_3 == b"\x00\x08\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x08\x00\x00", self.magic_3, self._io, u"/seq/2")
        self.song_id = self._io.read_u8le()
        self.instr_num = self._io.read_u4le()
        self.instr_mask = self._io.read_u4le()
        self.band_id = self._io.read_u8le()
        self.disc_id = self._io.read_u8le()
        self.year = self._io.read_u4le()
        self.song_name = (self._io.read_bytes(256)).decode(u"UTF-16")
        self.magic4 = self._io.read_bytes(4)
        if not self.magic4 == b"\x00\x08\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x08\x00\x00", self.magic4, self._io, u"/seq/10")
        self.magic5 = self._io.read_bytes(4)
        if not self.magic5 == b"\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self.magic5, self._io, u"/seq/11")
        self.trk_pts = []
        for i in range(5):
            self.trk_pts.append(self._io.read_u8le())

        self.diff_level = []
        for i in range(6):
            self.diff_level.append(self._io.read_u2le())

        self.trk_info = []
        for i in range(6):
            self.trk_info.append(self._io.read_u4le())

        self.meta_end = KaitaiStream.bytes_terminate(self._io.read_bytes(1660), 0, False)
        self.charts = []
        for i in range(self.instr_num):
            self.charts.append(Cbr.Track(self._io, self, self._root))


    class Charts(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.diff = KaitaiStream.resolve_enum(Cbr.DiffLvl, self._io.read_u4le())
            self.num_frets_pts = self._io.read_u4le()
            self.diff_info = self._io.read_u4le()
            self.pts_frets = []
            for i in range(self.num_frets_pts):
                self.pts_frets.append(self._io.read_u8le())

            self.frets_on_fire = []
            for i in range(self.num_frets_pts):
                self.frets_on_fire.append(Cbr.Color(self._io, self, self._root))



    class Track(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.inst_id = KaitaiStream.resolve_enum(Cbr.InstrumId, self._io.read_u4le())
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x00\x02\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x02\x00\x00", self.magic, self._io, u"/types/track/seq/1")
            self.start_diff_pos = self._io.read_u8le()
            self.num_pulse = self._io.read_u4le()
            self.start_pulse_pos = self._io.read_u8le()
            self.chart_info = KaitaiStream.bytes_terminate(self._io.read_bytes(484), 0, False)
            self.pulse = []
            for i in range(self.num_pulse):
                self.pulse.append(Cbr.Tick(self._io, self, self._root))

            if self.inst_id.value < 3:
                self.inst = Cbr.Instrument(self._io, self, self._root)

            if self.inst_id == Cbr.InstrumId.vocals:
                self.vocals = Cbr.Voice(self._io, self, self._root)



    class Voice(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x05\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x05\x00\x00\x00", self.magic, self._io, u"/types/voice/seq/0")
            self.num_waves_pts = self._io.read_u4le()
            self.start_wave_pos = self._io.read_u8le()
            self.num_lyrics_pts = self._io.read_u4le()
            self.start_lyrics_pos = self._io.read_u8le()
            self.vocal_info = KaitaiStream.bytes_terminate(self._io.read_bytes(100), 0, False)
            self.pts_wave = []
            for i in range(self.num_waves_pts):
                self.pts_wave.append(self._io.read_u8le())

            self.wave_form = []
            for i in range(self.num_waves_pts):
                self.wave_form.append(Cbr.Pitch(self._io, self, self._root))

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


    class Color(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_frets_wave = self._io.read_u4le()
            self.start_wave_pos = self._io.read_u8le()
            self.frets_wave = []
            for i in range(self.num_frets_wave):
                self.frets_wave.append(Cbr.Note(self._io, self, self._root))



    class Tick(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.time = self._io.read_u4le()
            self.type = self._io.read_u4le()


    class Note(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.time = self._io.read_u4le()
            self.len = self._io.read_u4le()
            self.mods = self._io.read_u4le()


    class Verse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_text = self._io.read_u4le()
            self.time_start = self._io.read_u4le()
            self.time_end = self._io.read_u4le()
            self.pts_to_pts = self._io.read_u8le()
            self.mods = self._io.read_u4le()
            self.len = self._io.read_u4le()
            self.pts_text = []
            for i in range(self.num_text):
                self.pts_text.append(self._io.read_u8le())

            self.text_block = []
            for i in range(self.num_text):
                self.text_block.append(Cbr.Syllable(self._io, self, self._root))



    class Pitch(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x02\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x02\x00\x00\x00", self.magic, self._io, u"/types/pitch/seq/0")
            self.next_pt = self._io.read_u8le()
            self.scale = self._io.read_u4le()
            self.start = self._io.read_u4le()
            self.end = self._io.read_u4le()
            self.mod = self._io.read_u4le()
            self.note = self._io.read_u4le()
            self.start_harm = self._io.read_u4le()
            self.note_harm = self._io.read_u4le()
            self.end_harm = self._io.read_u4le()


    class Instrument(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic_1 = self._io.read_bytes(4)
            if not self.magic_1 == b"\x02\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x02\x00\x00\x00", self.magic_1, self._io, u"/types/instrument/seq/0")
            self.magic_2 = self._io.read_bytes(4)
            if not self.magic_2 == b"\x03\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x03\x00\x00\x00", self.magic_2, self._io, u"/types/instrument/seq/1")
            self.diff_pts = []
            for i in range(15):
                self.diff_pts.append(self._io.read_u8le())

            self.diff_charts = []
            for i in range(3):
                self.diff_charts.append(Cbr.Charts(self._io, self, self._root))




