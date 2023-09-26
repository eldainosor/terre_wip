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
    4: band
    
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
    
seq:
  - id: magic_1
    contents: [0x76, 0x98, 0xCD, 0xAB]
  - id: magic_2
    contents: [0x00, 0x00, 0x04, 0x00]
  - id: magic_3
    contents: [0x00, 0x08, 0x00, 0x00]
    
  - id: song_id
    type: u8
  - id: instr_num
    type: u4
  - id: instr_mask
    type: u4
  - id: band_id
    type: u8
  - id: disc_id
    type: u8
  - id: year
    type: u4
  - id: song_name
    type: str
    size: 256
    encoding: UTF-16
    
  - id: magic4
    contents: [0x00, 0x08, 0x00, 0x00]
  - id: magic5
    contents: [0x00, 0x00, 0x00, 0x00]
  
  - id: trk_pts
    type: u8
    repeat: expr
    repeat-expr: 5
    
  - id: diff_level
    type: u2
    repeat: expr
    repeat-expr: 6
  
  - id: trk_info
    type: u4
    repeat: expr
    repeat-expr: 6
    doc: Variable not decoded yet
    
  - id: meta_end  
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

      - id: magic
        contents: [0x00, 0x02, 0x00, 0x00]
        
      - id: start_diff_pos
        type: u8
        
      - id: num_pulse
        type: u4
        
      - id: start_pulse_pos
        type: u8
             
      - id: chart_info
        terminator: 0
        size: 484
        doc: Variable not decoded yet
        
      - id: pulse
        type: tick
        repeat: expr
        repeat-expr: num_pulse
      
      - id: inst
        if: inst_id.to_i < 3
        type: instrument
        
      - id: vocals
        if: inst_id == instrum_id::vocals
        type: voice

  tick:
    seq:
      - id: time
        type: u4
      - id: type
        type: u4
        
  instrument:
    seq:
      - id: magic_1
        contents: [0x02, 0x00, 0x00, 0x00]
      - id: magic_2
        contents: [0x03, 0x00, 0x00, 0x00]

      - id: diff_pts
        type: u8
        repeat: expr
        repeat-expr: 15

      - id: diff_charts
        type: charts
        repeat: expr
        repeat-expr: 3
        
  charts:
    seq:
      - id: diff
        type: u4
        enum: diff_lvl
        
      - id: num_frets_pts
        type: u4
        
      - id: diff_info
        type: u4
        
      - id: pts_frets
        type: u8		
        repeat: expr
        repeat-expr: num_frets_pts
        
      - id: frets_on_fire
        type: color
        repeat: expr
        repeat-expr: num_frets_pts
        
  color:
    seq:
      - id: num_frets_wave
        type: u4
        
      - id: start_wave_pos
        type: u8
        
      - id: frets_wave
        type: note
        repeat: expr
        repeat-expr: num_frets_wave
        
  note:
    seq:
      - id: time
        type: u4
      - id: len
        type: u4
      - id: mods
        type: u4
        
  voice:
    seq:
      - id: magic
        contents: [0x05, 0x00, 0x00, 0x00]
        
      - id: num_waves_pts
        type: u4
      - id: start_wave_pos
        type: u8
      - id: num_lyrics_pts
        type: u4
      - id: start_lyrics_pos
        type: u8
        
      - id: vocal_info
        size: 100
        terminator: 0
        doc: Variable not decoded yet

      - id: pts_wave
        type: u8
        repeat: expr
        repeat-expr: num_waves_pts

      - id: wave_form
        type: pitch
        repeat: expr
        repeat-expr: num_waves_pts
        
      - id: pts_lyrics
        type: u8
        repeat: expr
        repeat-expr: num_lyrics_pts

      - id: lyrics
        type: verse
        repeat: expr
        repeat-expr: num_lyrics_pts
        
  pitch:
    seq:
      - id: magic
        contents: [0x02, 0x00, 0x00, 0x00]
        
      - id: next_pt
        type: u8
        
      - id: scale
        type: u4
      - id: start
        type: u4
      - id: end
        type: u4
      - id: mod
        type: u4
      - id: note
        type: u4
        
      - id: start_harm
        type: u4
      - id: note_harm
        type: u4
      - id: end_harm
        type: u4

  verse:
    seq:
      - id: num_text
        type: u4
      
      - id: time_start
        type: u4
      - id: time_end
        type: u4
      
      - id: pts_to_pts
        type: u8
        
      - id: mods
        type: u4
      
      - id: len
        type: u4
        
      - id: pts_text
        type: u8
        repeat: expr
        repeat-expr: num_text
      
      - id: text_block
        type: syllable
        repeat: expr
        repeat-expr: num_text
        
  syllable:
    seq:        
      - id: time_start
        type: u4
      - id: time_end
        type: u4
      - id: type
        type: u4
      - id: text
        type: strz
        encoding: WINDOWS-1252
        