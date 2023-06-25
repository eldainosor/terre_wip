meta:
  id: cbr
  file-extension: cbr
  endian: le

seq:
  - id: hdr
    type: header
  - id: tracks
    type: track
    
types:
  header:
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
      
      - id: pointers
        type: u8
        repeat: expr
        repeat-expr: 217
        doc: pointers to the END of each instrument's tracks

      - id: guitar
        type: instrument
        size: ( pointers[0] - 0x800 )
      - id: rhythm
        type: instrument
        size: ( pointers[1] - pointers[0] )
      - id: drums
        type: instrument
        size: ( pointers[2] - pointers[1] )
      - id: voice
        type: voice
        if: pointers[3] != 0
        size: ( pointers[3] - pointers[2] )
        
      - id: extras
        type: separator
        if: pointers[3] != 0
        size-eos: true
        
      - id: voice2
        type: voice
        if: pointers[3] == 0
        size-eos: true
        
  separator:
    seq:
      - id: id
        type: u8
        
      - id: end_pos
        type: u8
      - id: size_bytes
        type: u4
      - id: start_pos
        type: u8
      - id: fill
        type: u4
        repeat: expr
        repeat-expr: 121
        
      - id: head
        type: body
        repeat: expr
        repeat-expr: size_bytes

  body:
    seq:
      - id: val
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
        type: u8

      - id: diff_point
        type: u8
        repeat: expr
        repeat-expr: 15
        doc: pointers to the END of each difficulty chart for this instrument
        
      - id: easy
        type: array
        size: ( diff_point[1] - diff_point[0] )
        
      - id: norm
        type: array
        size: ( diff_point[2] - diff_point[1] )

      - id: hard
        type: array
        size-eos: true
        
  frets:
    seq:
      - id: lo
        type: u4
      - id: me
        type: u4
      - id: hi
        type: u4
        
  array:
    seq:
      - id: song
        type: u4
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
      
      - id: zeros
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
    