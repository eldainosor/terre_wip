meta:
  id: cbr
  file-extension: cbr
  endian: le
        
enums:
  diff_lvl:
    0: easy
    1: medium
    2: hard

  instrum_id:
    0: guitar
    1: rhythm
    2: drums
    3: vocals
    4: song
    
  pos_id:
    0: lo
    1: me
    2: hi

  color_id:
    0: orange
    1: blue
    2: yellow
    3: red
    4: green
  
  # The overdrive flag is just to indicate the note is within a overdrive phrase.
  note_modifiers:
    0: regular
    1: overdrive
    2: undocumented_yet
    16: hopo
    17: hopo_and_overdrive
    32: force_upstrum
    33: force_upstrum_and_overdrive
    48: force_downstrum
    49: force_downstrum_and_overdrive 
seq:
  - id: magic_1
    contents: [0x76, 0x98, 0xCD, 0xAB]
  - id: flags
    contents: [0x00, 0x00, 0x04, 0x00]
  - id: header_size
    contents: [0x00, 0x08, 0x00, 0x00]
    
  - id: apidata_song_id
    type: u8
  - id: instr_num
    type: u4
  - id: instr_mask
    type: u4
  - id: apidata_banda
    type: u8
  - id: apidata_disco
    type: u8
  - id: apidata_anio
    type: u4
  - id: apidata_cancion
    type: str
    size: 256
    encoding: UTF-16LE
    
  - id: section_header_size_confirm
    contents: [0x00, 0x08, 0x00, 0x00]
  - id: magic5
    contents: [0x00, 0x00, 0x00, 0x00]
  
  - id: instrument_charts_offset
    type: u8
    repeat: expr
    repeat-expr: 5
    
  - id: apidata_diff_guitarra
    type: u2
  - id: apidata_diff_bajo
    type: u2
  - id: apidata_diff_bateria
    type: u2
  - id: apidata_diff_voz
    type: u2
  - id: apidata_extra_1 # Para completar los 6 que requiere el formato
    type: u2
  - id: apidata_extra_2
    type: u2
  
  - id: instrument_ids
    type: u4
    repeat: expr
    repeat-expr: 6
    doc: Variable not decoded yet
    
  - id: header_padding  
    terminator: 0
    size: 1660  
    doc: Variable not decoded yet
    
  - id: charts
    type: track
    repeat: expr
    repeat-expr: instr_num 
    
types:
  track:
    seq:
      - id: inst_id
        type: u4
        enum: instrum_id

      - id: magic_section
        contents: [0x00, 0x02, 0x00, 0x00]
        
      - id: start_diff_pos
        type: u8
        doc: Variable not decoded yet
        
      - id: beatmap_data_size
        type: u4
        
      - id: beatmap_data_offset
        type: u8
             
      - id: chart_section_padding
        terminator: 0
        size: 484
        
      - id: beatmap_data
        type: song_beat
        repeat: expr
        repeat-expr: beatmap_data_size
      
      - id: inst
        if: inst_id.to_i < 3
        type: track_instrument
        
      - id: vocals
        if: inst_id == instrum_id::vocals
        type: track_mic

  song_beat:
    seq:
      - id: tick
        type: u4
      - id: beat_count
        type: u4
        
  # This is named this way on the game engine
  track_instrument:
    seq:
      - id: magic_1
        contents: [0x02, 0x00, 0x00, 0x00]
      - id: magic_2
        contents: [0x03, 0x00, 0x00, 0x00]

      - id: diff_charts_offsets
        type: u8
        repeat: expr
        repeat-expr: 3
        
      - id: diff_offsets_padding
        terminator: 0
        size: 96

      - id: diff_charts
        type: charts
        repeat: expr
        repeat-expr: 3
        
  charts:
    seq:
      - id: diff
        type: u4
        enum: diff_lvl
        
      - id: lane_count
        type: u4
        
      - id: diff_info
        type: u4
        doc: maybe it's diff section size?
        
      - id: fret_lane_sections_offset
        type: u8		
        repeat: expr
        repeat-expr: lane_count
        
      - id: lane_data
        type: fret_lane
        repeat: expr
        repeat-expr: lane_count
        doc: every array number it's declared in color_id
        
  fret_lane:
    seq:
      - id: amont_notes_in_lane
        type: u4
        
      - id: notes_data_size
        type: u8
        
      - id: lane_notes
        type: note
        repeat: expr
        repeat-expr: amont_notes_in_lane
        
  note:
    seq:
      - id: tick
        type: u4
      - id: length
        type: u4
      - id: modifiers
        type: u4
    instances:
        note_attribute:
          value: modifiers
          enum: note_modifiers
        
  # This is named this way on the game engine
  track_mic:
    seq:
      - id: magic
        contents: [0x05, 0x00, 0x00, 0x00]
        
      - id: vocal_notes_data_size
        type: u4
      - id: vocal_notes_table_offset
        type: u8
      - id: vocal_phrases_data_size
        type: u4
      - id: vocal_phrases_table_offset
        type: u8
        
      - id: vocal_padding
        size: 100
        terminator: 0
        doc: Variable not decoded yet

      - id: pitch_note_pointers
        type: u8
        repeat: expr
        repeat-expr: vocal_notes_data_size

      - id: pitch_note_data
        type: pitch
        repeat: expr
        repeat-expr: vocal_notes_data_size
        
      - id: phrase_pointers
        type: u8
        repeat: expr
        repeat-expr: vocal_phrases_data_size

      - id: phrase_data
        type: verse
        repeat: expr
        repeat-expr: vocal_phrases_data_size
        
  pitch:
    seq:
      - id: magic
        contents: [0x02, 0x00, 0x00, 0x00]
        
      - id: self_ptr
        type: u8
        
      - id: scale
        type: u4
      - id: tick_start
        type: u4
      - id: tick_end
        type: u4
      - id: modifiers
        type: u4
      - id: note
        type: u4
        
      - id: tick_start_copy
        type: u4
      - id: note_copy
        type: u4
      - id: tick_end_copy
        type: u4

  verse:
    seq:
      - id: num_syllables
        type: u4
      
      - id: tick_start
        type: u4
      - id: tick_end
        type: u4
      
      - id: next_ptr
        type: u8
        
      - id: overdrive_flag
        type: u4
      
      - id: length
        type: u4
        
      - id: syllable_pointers
        type: u8
        repeat: expr
        repeat-expr: num_syllables
      
      - id: syllables_text
        type: syllable
        repeat: expr
        repeat-expr: num_syllables
        
  syllable:
    seq:        
      - id: tick_start
        type: u4
      - id: tick_end
        type: u4
      - id: spoken_flag
        type: u4
      - id: text
        type: strz
        encoding: WINDOWS-1252
        