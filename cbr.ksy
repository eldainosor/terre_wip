meta:
  id: cbr
  file-extension: cbr
  endian: le
        
enums:
  inst_id:
    0: guitar
    1: rhythm
    2: drums
    3: voice
    4: band

  diff_lvl:
    0: easy
    1: norm
    2: hard
    
    
  pos_id:
    0: lo
    1: me
    2: hi
    
seq:
  - id: info
    type: meta_data
  - id: tracks
    type: track
    
types:
  meta_data:
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
        
  track:
    seq:
      - id: magic
        contents: [0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      
      - id: trk_pts
        type: u8
        repeat: expr
        repeat-expr: 5
        doc: pointers to the END of each instrument's tracks
      
      - id: diff_level
        type: u2
        repeat: expr
        repeat-expr: 6
      
      - id: trk_info
        type: u4
        repeat: expr
        repeat-expr: 6
        
      - id: trk_vol
        type: u4
      
      - id: nulos  
        terminator: 0
        size: 1656
        doc: Variable not decoded yet
        
      - id: charts
        type: instrument
        repeat: expr
        repeat-expr: 3
        
      - id: vocals
        type: voice
        if: trk_info[3] == 3
        
      - id: band
        type: header
        if: trk_info[4] == 4
        
  header:
    seq:
      - id: instrument_id
        type: u4
        enum: inst_id

      - id: magic
        contents: [0x00, 0x02, 0x00, 0x00]
        
      - id: start_diff_pos
        type: u8
        
      - id: num_events
        type: u4
        
      - id: start_events_pos
        type: u8
             
      - id: bpm
        type: u4
        
      - id: nulos
        terminator: 0
        size: 480
        doc: Variable not decoded yet
        
      - id: events
        type: event
        repeat: expr
        repeat-expr: num_events

  event:
    seq:
      - id: time
        type: u4
        
      - id: type
        type: u4
        
  instrument:
    seq:
      - id: head
        type: header
      
      - id: magic_1
        contents: [0x02, 0x00, 0x00, 0x00]
      - id: magic_2
        contents: [0x03, 0x00, 0x00, 0x00]

      - id: diff_pts
        type: u8
        repeat: expr
        repeat-expr: 15
        doc: pointers to the END of each difficulty chart for this instrument

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
        
      - id: speed
        type: u4
        
      - id: pts_frets
        type: u8		
        repeat: expr
        repeat-expr: num_frets_pts
        
      - id: frets_on_fire
        type: frets	
        repeat: expr
        repeat-expr: num_frets_pts
        
  frets:
    seq:
      - id: num_frets_wave
        type: u4
        
      - id: pts_start_wave
        type: u8
        
      - id: frets_wave
        type: spark
        repeat: expr
        repeat-expr: num_frets_wave
        
  spark:
    seq:
      - id: timing
        type: u4
        
      - id: len
        type: u4
        
      - id: type
        type: u4
        
  voice:
    seq:
      - id: head
        type: header
      
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
        
      - id: speed
        type: u4

      - id: nulos
        size: 96
        terminator: 0
        doc: Variable not decoded yet
        
      - id: pts_wave
        type: u8
        repeat: expr
        repeat-expr: num_waves_pts

      - id: wave_form
        type: flow
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
        
  flow:
    seq:
      - id: magic
        contents: [0x02, 0x00, 0x00, 0x00]
        
      - id: next_pt
        type: u8
        
      - id: water
        type: u4
        repeat: expr
        repeat-expr: 8
        doc: Is this timing?

  verse:
    seq:
      - id: num_text
        type: u4
      
      - id: info
        type: u4
        repeat: expr
        repeat-expr: 6
      
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
        