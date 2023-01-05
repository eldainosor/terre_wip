meta:
  id: cbr
  file-extension: cbr
  endian: le

seq:
  - id: header
    type: header
  - id: charts
    type: charts
    
types:
  header:
    seq:
      - id: magic
        contents: [0x76, 0x98, 0xCD, 0xAB]
      - id: flags_1
        size: 8
      - id: song_id
        type: u8
      - id: flags_2
        size: 8
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
        
  charts:
    seq:
      - id: magic
        contents: [0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      
      - id: pointer
        type: u8
        repeat: expr
        repeat-expr: 4
        doc: Pointer to the END of each instrument's charts
        
      - id: info
        size: 4
        repeat: expr
        repeat-expr: 12
      - id: zeros
        size: 0x678
  
      - id: guitar
        type: instrument
        size: ( pointer[0] - 0x800 )
      - id: rhythm
        type: instrument
        size: ( pointer[1] - pointer[0] )
      - id: drums
        type: instrument
        size: ( pointer[2] - pointer[1] )
      - id: voice
        type: voice
        size: ( pointer[3] - pointer[2] ) 
        
      - id: extras
        type: separator
        size-eos: true
        
  separator:
    seq:
      - id: id
        size: 8
        
      - id: end_pos
        type: u8
      - id: size_bytes
        type: u4
      - id: start_pos
        type: u8
      - id: fill
        type: u4

      - id: zeros
        size: 0x1E0
        
      - id: head
        type: body
        repeat: expr
        repeat-expr: size_bytes

  body:
    seq:
      - id: value
        type: u2
      - id: len
        type: u2
      - id: num
        type: u4

  instrument:
    seq:
      - id: header
        type: separator
      
      - id: info
        size: 8

      - id: diff_point
        type: u8
        repeat: expr
        repeat-expr: 3
        doc: Pointer to the END of each difficulty chart for this instrument
        
      - id: zeros
        size: 96
        
      - id: easy
        type: array
        size: ( diff_point[1] - diff_point[0] ) 
        
      - id: normal
        type: array
        size: ( diff_point[2] - diff_point[1] ) 

      - id: hard
        type: array
        size-eos: true
        
  frets:
    seq:
      - id: notes
        type: u4
        doc: TODO Should be 12bytes
        
  array:
    seq:
      - id: song
        type: frets
        repeat: eos
        
  voice:
    seq:
      - id: header
        type: separator
      
      - id: info
        size: 8

      - id: start_pitch_pos
        type: u8
      - id: pitch_vol
        type: u4
      - id: start_lyrics_pos
        type: u8
      - id: lyrics_vol
        type: u4
      
      - id: zeros
        size: 96
        
      - id: pitch_pts
        type: array
        size: start_lyrics_pos - start_pitch_pos
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
    1: normal
    2: hard
    