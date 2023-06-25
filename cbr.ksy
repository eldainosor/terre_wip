meta:
  id: cbr
  file-extension: cbr
  endian: le

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
        encoding: UTF-16
        size: 0x100
        
  track:
    seq:
      - id: magic
        contents: [0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      
      - id: trk_pts
        type: u8
        repeat: expr
        repeat-expr: 217
        doc: pointers to the END of each instrument's tracks

      - id: guitar
        type: instrument
        size: ( trk_pts[0] - 0x800 )
      - id: rhythm
        type: instrument
        size: ( trk_pts[1] - trk_pts[0] )
      - id: drums
        type: instrument
        size: ( trk_pts[2] - trk_pts[1] )
      - id: voice
        type: voice
        if: trk_pts[3] != 0
        size: ( trk_pts[3] - trk_pts[2] )
        
      - id: extras
        type: separator
        if: trk_pts[3] != 0
        size-eos: true
        
      - id: voice2
        type: voice
        if: trk_pts[3] == 0
        size-eos: true
        
  separator:
    seq:
      - id: channel
        type: u8
        
      - id: end_pos
        type: u8
      - id: size_bytes
        type: u4
      - id: start_pos
        type: u8
      
      - id: bpm
        type: u4        
      
      - id: zeros60
        type: u8
        repeat: expr
        repeat-expr: 60
        
      - id: events
        type: event
        repeat: expr
        repeat-expr: size_bytes

  event:
    seq:
      - id: val
        size: 8
        
  instrument:
    seq:
      - id: header
        type: separator
      
      - id: magic
        contents: [0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00]

      - id: diff_pts
        type: u8
        repeat: expr
        repeat-expr: 15
        doc: pointers to the END of each difficulty chart for this instrument
        
      - id: easy
        type: array
        size: ( diff_pts[1] - diff_pts[0] )
        
      - id: norm
        type: array
        size: ( diff_pts[2] - diff_pts[1] )

      - id: hard
        type: array
        size-eos: true
        
  frets:
    seq:
      - id: fret
        size: 4
        
  array:
    seq:
      - id: song
        type: frets
        repeat: eos
        doc: NOTE should be 12 bytes
        
  voice:
    seq:
      - id: header
        type: separator
      
      - id: info
        type: u8

      - id: start_wave_pos
        type: u8
      - id: wave_vol
        type: u4
      - id: start_lyrics_pos
        type: u8
      - id: lyrics_vol
        type: u4
      
      - id: zeros12
        type: u8
        repeat: expr
        repeat-expr: 12
        
      - id: wave_pts
        type: array
        size: start_lyrics_pos - start_wave_pos 
        doc: TODO pitch_pts[0] is pointing first next struct of notes in 12bytes
        
      - id: lyrics
        doc: TODO String+null+12bytes
        size-eos: true

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
    