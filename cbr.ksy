meta:
  id: cbr
  file-extension: cbr
  endian: le
  imports:
    - /common/vlq_base128_be

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
        
      - id: end_pos
        type: u8
      - id: size_bytes
        type: u4
      - id: start_pos
        type: u8
             
      - id: bpm
        terminator: 0
        size: 484
        
      - id: events
        type: event
        repeat: expr
        repeat-expr: size_bytes

  event:
    seq:
      - id: val
        type: u2
      
      - id: cont
        type: u2
        
      - id: pos
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
        type: array
        size: diff_pts[1] - diff_pts[0]
        
      - id: norm
        type: array
        size: diff_pts[2] - diff_pts[1]

      - id: hard
        type: array
        size-eos: true
        
  array:
    seq:
      - id: song
        type: notes
        repeat: eos
        doc: NOTE should be 12 bytes
  
  notes:
    seq:
      - id: foo
        type: u2
      - id: bar
        type: u1
      - id: nulo
        type: u1
  
  voice:
    seq:
      - id: hdr
        type: header
      
      - id: info
        type: u8

      - id: start_wave_pos
        type: u8
      - id: wave_vol
        type: u4
      - id: start_lyrics_pos
        type: u8
      - id: lyrics_vol
        terminator: 0
        size: 100
        
      - id: norm
        type: array
        size: start_lyrics_pos - start_wave_pos 
        doc: TODO pitch_pts[0] is pointing first next struct of notes in 12bytes
        
      - id: lyrics
        size-eos: true

  verse:
    seq:
      - id: start
        type: u2
      - id: line_in
        type: u2
      - id: end
        type: u2
      - id: line_out
        type: u2
      - id: verse_type2
        type: u2
      - id: verse_type3
        type: u2
      - id: text
        type: strz
        if: start < end
        encoding: ASCII

enums:
  inst_id:
    0: guitar
    1: rhythm
    2: drums
    3: voice
    4: song

enums:
  diff_id:
    0: easy
    1: norm
    2: hard
    
enums:
  pos_id:
    0: lo
    1: me
    2: hi
    