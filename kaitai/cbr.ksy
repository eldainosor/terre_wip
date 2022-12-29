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
  
      - id: chart_guitar
        type: instrument
        size: pointer[0] - 0x800
      - id: chart_rhythm
        type: instrument
        size: pointer[1] - pointer[0]
      - id: chart_drums
        type: instrument
        size: pointer[2] - pointer[1]
      - id: chart_voice
        type: voice
        size: pointer[3] - pointer[2]
        
      - id: end_of_charts
        type: chart_head
        size-eos: true
        
  chart_head:
    seq:
      - id: id
        size: 8
        
      - id: end_head_pos
        type: u8
      - id: size_head_bytes
        type: u4
      - id: start_head_pos
        type: u8
      - id: size_zero_fill
        type: u4

      - id: zeros
        size: 0x1E0
        
      - id: head
        type: head_body
        repeat: expr
        repeat-expr: size_head_bytes

  head_body:
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
        type: chart_head
      
      - id: info
        size: 8

      - id: diff_point
        type: u8
        repeat: expr
        repeat-expr: 3
        doc: Pointer to the END of each difficulty chart for this instrument
        
      - id: zeros
        size: 96
        
      - id: chart_easy
        type: chart_array
        size: diff_point[1] - diff_point[0]
        
      - id: chart_med
        type: chart_array
        size: diff_point[2] - diff_point[1]

      - id: chart_hard
        type: chart_array
        size-eos: true
        
  chart_body:
    seq:
      - id: notes
        type: u4
        doc: TODO Should be 12bytes
        
  chart_array:
    seq:
      - id: song
        type: chart_body
        repeat: eos
        
  voice:
    seq:
      - id: header
        type: chart_head
      
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
        type: chart_array
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
    1: med
    2: hard
    