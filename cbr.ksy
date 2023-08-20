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
    4: song

enums:
  pos_id:
    0: lo
    1: me
    2: hi

enums:
  diff_lvl:
    0: easy
    1: norm
    2: hard
    
seq:
  - id: info
    type: meta_data
  - id: tracks
    type: track
    
types:
  meta_data:
    seq:
      - id: magic
        contents: [0x76, 0x98, 0xCD, 0xAB]
      - id: flags_1
        type: u8
      - id: song_id
        type: u8
      - id: flags_2
        type: u8
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
        terminator: 0
        size: 1660
        
      - id: guitar
        type: instrument
        if: trk_pts[0] != 0
        size: trk_pts[0] - 0x800
      - id: rhythm
        type: instrument
        if: trk_pts[1] != 0
        size: trk_pts[1] - trk_pts[0]
      - id: drums
        type: instrument
        if: trk_pts[2] != 0
        size: trk_pts[2] - trk_pts[1]
        
      - id: vocals_with_extras
        type: voice
        if: trk_pts[3] != 0
        size:  trk_pts[3] - trk_pts[2]
      - id: extras
        type: header
        if: trk_pts[3] != 0
        
      - id: vocals_no_extras
        type: voice
        if: trk_pts[3] == 0
        size-eos: true
        
  header:
    seq:
      - id: instrument_id
        type: u4
        enum: inst_id

      - id: channel
        type: u4
        
      - id: start_diff_pos
        type: u8
        
      - id: num_events
        type: u4
        
      - id: start_events_pos
        type: u8
             
      - id: bpm
        terminator: 0
        size: 484
        
      - id: events
        type: event
        repeat: expr
        repeat-expr: num_events

  event:
    seq:
      - id: count
        type: u4
        
      - id: type
        type: u4
        
  instrument:
    seq:
      - id: hdr
        type: header
      
      - id: magic
        contents: [0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00]

      - id: diff_pts
        type: u8
        repeat: expr
        repeat-expr: 15
        doc: pointers to the END of each difficulty chart for this instrument

      - id: easy
        type: charts
      - id: norm
        type: charts
      - id: hard
        type: charts
        
  charts:
    seq:
      - id: diff
        type: u4
        
      - id: num_frets_pts
        type: u4
        
      - id: time_start
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
      - id: fire
        type: u4
        repeat: expr
        repeat-expr: 3

  array:
    seq:
      - id: song
        type: notes
        repeat: eos
        doc: NOTE should be 12 bytes        
        
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

  lister:
    seq:
      - id: pointers
        type: u8
        repeat: eos
        doc: NOTE should be 12 bytes
        
  notes:
    seq:
      - id: foo
        type: u2
      - id: bar
        type: u2
  
  voice:
    seq:
      - id: hdr
        type: header
      
      - id: magic1
        contents: [0x05, 0x00, 0x00, 0x00]
        
      - id: num_waves_pts
        type: u4
        
      - id: start_wave_pos
        type: u8
        
      - id: num_lyrics_pts
        type: u4
        
      - id: start_lyrics_pos
        type: u8
        
      - id: lyrics_info
        size: 100
        
      - id: pts_wave
        type: u8
        repeat: expr
        repeat-expr: num_waves_pts

      - id: elements
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

    