# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cbr(KaitaiStruct):

    class ColorId(IntEnum):
        orange = 0
        blue = 1
        yellow = 2
        red = 3
        green = 4

    class DiffLvl(IntEnum):
        easy = 0
        medium = 1
        hard = 2

    class InstrumId(IntEnum):
        guitar = 0
        rhythm = 1
        drums = 2
        vocals = 3
        song = 4

    class NoteModifiers(IntEnum):
        regular = 0
        overdrive = 1
        undocumented_yet = 2
        hopo = 16
        hopo_and_overdrive = 17
        force_upstrum = 32
        force_upstrum_and_overdrive = 33
        force_downstrum = 48
        force_downstrum_and_overdrive = 49

    class PosId(IntEnum):
        lo = 0
        me = 1
        hi = 2
    def __init__(self, _io, _parent=None, _root=None):
        super(Cbr, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.magic_1 = self._io.read_bytes(4)
        if not self.magic_1 == b"\x76\x98\xCD\xAB":
            raise kaitaistruct.ValidationNotEqualError(b"\x76\x98\xCD\xAB", self.magic_1, self._io, u"/seq/0")
        self.flags = self._io.read_bytes(4)
        if not self.flags == b"\x00\x00\x04\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x04\x00", self.flags, self._io, u"/seq/1")
        self.header_size = self._io.read_bytes(4)
        if not self.header_size == b"\x00\x08\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x08\x00\x00", self.header_size, self._io, u"/seq/2")
        self.apidata_song_id = self._io.read_u8le()
        self.instr_num = self._io.read_u4le()
        self.instr_mask = self._io.read_u4le()
        self.apidata_banda = self._io.read_u8le()
        self.apidata_disco = self._io.read_u8le()
        self.apidata_anio = self._io.read_u4le()
        self.apidata_cancion = (self._io.read_bytes(256)).decode(u"UTF-16LE")
        self.section_header_size_confirm = self._io.read_bytes(4)
        if not self.section_header_size_confirm == b"\x00\x08\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x08\x00\x00", self.section_header_size_confirm, self._io, u"/seq/10")
        self.magic5 = self._io.read_bytes(4)
        if not self.magic5 == b"\x00\x00\x00\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00\x00\x00\x00", self.magic5, self._io, u"/seq/11")
        self.instrument_charts_offset = []
        for i in range(5):
            self.instrument_charts_offset.append(self._io.read_u8le())

        self.apidata_diff_guitarra = self._io.read_u2le()
        self.apidata_diff_bajo = self._io.read_u2le()
        self.apidata_diff_bateria = self._io.read_u2le()
        self.apidata_diff_voz = self._io.read_u2le()
        self.apidata_extra_1 = self._io.read_u2le()
        self.apidata_extra_2 = self._io.read_u2le()
        self.instrument_ids = []
        for i in range(6):
            self.instrument_ids.append(self._io.read_u4le())

        self.header_padding = KaitaiStream.bytes_terminate(self._io.read_bytes(1660), 0, False)
        self.charts = []
        for i in range(self.instr_num):
            self.charts.append(Cbr.Track(self._io, self, self._root))



    def _fetch_instances(self):
        pass
        for i in range(len(self.instrument_charts_offset)):
            pass

        for i in range(len(self.instrument_ids)):
            pass

        for i in range(len(self.charts)):
            pass
            self.charts[i]._fetch_instances()


    class Charts(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.Charts, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.diff = KaitaiStream.resolve_enum(Cbr.DiffLvl, self._io.read_u4le())
            self.lane_count = self._io.read_u4le()
            self.diff_info = self._io.read_u4le()
            self.fret_lane_sections_offset = []
            for i in range(self.lane_count):
                self.fret_lane_sections_offset.append(self._io.read_u8le())

            self.lane_data = []
            for i in range(self.lane_count):
                self.lane_data.append(Cbr.FretLane(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.fret_lane_sections_offset)):
                pass

            for i in range(len(self.lane_data)):
                pass
                self.lane_data[i]._fetch_instances()



    class FretLane(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.FretLane, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.amont_notes_in_lane = self._io.read_u4le()
            self.notes_data_size = self._io.read_u8le()
            self.lane_notes = []
            for i in range(self.amont_notes_in_lane):
                self.lane_notes.append(Cbr.Note(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.lane_notes)):
                pass
                self.lane_notes[i]._fetch_instances()



    class Note(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.Note, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tick = self._io.read_u4le()
            self.length = self._io.read_u4le()
            self.modifiers = self._io.read_u4le()


        def _fetch_instances(self):
            pass

        @property
        def note_attribute(self):
            if hasattr(self, '_m_note_attribute'):
                return self._m_note_attribute

            self._m_note_attribute = KaitaiStream.resolve_enum(Cbr.NoteModifiers, self.modifiers)
            return getattr(self, '_m_note_attribute', None)


    class Pitch(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.Pitch, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x02\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x02\x00\x00\x00", self.magic, self._io, u"/types/pitch/seq/0")
            self.self_ptr = self._io.read_u8le()
            self.scale = self._io.read_u4le()
            self.tick_start = self._io.read_u4le()
            self.tick_end = self._io.read_u4le()
            self.modifiers = self._io.read_u4le()
            self.note = self._io.read_u4le()
            self.tick_start_copy = self._io.read_u4le()
            self.note_copy = self._io.read_u4le()
            self.tick_end_copy = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class SongBeat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.SongBeat, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tick = self._io.read_u4le()
            self.beat_count = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class Syllable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.Syllable, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.tick_start = self._io.read_u4le()
            self.tick_end = self._io.read_u4le()
            self.spoken_flag = self._io.read_u4le()
            self.text = (self._io.read_bytes_term(0, False, True, True)).decode(u"windows-1252")


        def _fetch_instances(self):
            pass


    class Track(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.Track, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.inst_id = KaitaiStream.resolve_enum(Cbr.InstrumId, self._io.read_u4le())
            self.magic_section = self._io.read_bytes(4)
            if not self.magic_section == b"\x00\x02\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00\x02\x00\x00", self.magic_section, self._io, u"/types/track/seq/1")
            self.start_diff_pos = self._io.read_u8le()
            self.beatmap_data_size = self._io.read_u4le()
            self.beatmap_data_offset = self._io.read_u8le()
            self.chart_section_padding = KaitaiStream.bytes_terminate(self._io.read_bytes(484), 0, False)
            self.beatmap_data = []
            for i in range(self.beatmap_data_size):
                self.beatmap_data.append(Cbr.SongBeat(self._io, self, self._root))

            if int(self.inst_id) < 3:
                pass
                self.inst = Cbr.TrackInstrument(self._io, self, self._root)

            if self.inst_id == Cbr.InstrumId.vocals:
                pass
                self.vocals = Cbr.TrackMic(self._io, self, self._root)



        def _fetch_instances(self):
            pass
            for i in range(len(self.beatmap_data)):
                pass
                self.beatmap_data[i]._fetch_instances()

            if int(self.inst_id) < 3:
                pass
                self.inst._fetch_instances()

            if self.inst_id == Cbr.InstrumId.vocals:
                pass
                self.vocals._fetch_instances()



    class TrackInstrument(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.TrackInstrument, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic_1 = self._io.read_bytes(4)
            if not self.magic_1 == b"\x02\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x02\x00\x00\x00", self.magic_1, self._io, u"/types/track_instrument/seq/0")
            self.magic_2 = self._io.read_bytes(4)
            if not self.magic_2 == b"\x03\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x03\x00\x00\x00", self.magic_2, self._io, u"/types/track_instrument/seq/1")
            self.diff_charts_offsets = []
            for i in range(3):
                self.diff_charts_offsets.append(self._io.read_u8le())

            self.diff_offsets_padding = KaitaiStream.bytes_terminate(self._io.read_bytes(96), 0, False)
            self.diff_charts = []
            for i in range(3):
                self.diff_charts.append(Cbr.Charts(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.diff_charts_offsets)):
                pass

            for i in range(len(self.diff_charts)):
                pass
                self.diff_charts[i]._fetch_instances()



    class TrackMic(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.TrackMic, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x05\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x05\x00\x00\x00", self.magic, self._io, u"/types/track_mic/seq/0")
            self.vocal_notes_data_size = self._io.read_u4le()
            self.vocal_notes_table_offset = self._io.read_u8le()
            self.vocal_phrases_data_size = self._io.read_u4le()
            self.vocal_phrases_table_offset = self._io.read_u8le()
            self.vocal_padding = KaitaiStream.bytes_terminate(self._io.read_bytes(100), 0, False)
            self.pitch_note_pointers = []
            for i in range(self.vocal_notes_data_size):
                self.pitch_note_pointers.append(self._io.read_u8le())

            self.pitch_note_data = []
            for i in range(self.vocal_notes_data_size):
                self.pitch_note_data.append(Cbr.Pitch(self._io, self, self._root))

            self.phrase_pointers = []
            for i in range(self.vocal_phrases_data_size):
                self.phrase_pointers.append(self._io.read_u8le())

            self.phrase_data = []
            for i in range(self.vocal_phrases_data_size):
                self.phrase_data.append(Cbr.Verse(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.pitch_note_pointers)):
                pass

            for i in range(len(self.pitch_note_data)):
                pass
                self.pitch_note_data[i]._fetch_instances()

            for i in range(len(self.phrase_pointers)):
                pass

            for i in range(len(self.phrase_data)):
                pass
                self.phrase_data[i]._fetch_instances()



    class Verse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Cbr.Verse, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.num_syllables = self._io.read_u4le()
            self.tick_start = self._io.read_u4le()
            self.tick_end = self._io.read_u4le()
            self.next_ptr = self._io.read_u8le()
            self.overdrive_flag = self._io.read_u4le()
            self.length = self._io.read_u4le()
            self.syllable_pointers = []
            for i in range(self.num_syllables):
                self.syllable_pointers.append(self._io.read_u8le())

            self.syllables_text = []
            for i in range(self.num_syllables):
                self.syllables_text.append(Cbr.Syllable(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.syllable_pointers)):
                pass

            for i in range(len(self.syllables_text)):
                pass
                self.syllables_text[i]._fetch_instances()
