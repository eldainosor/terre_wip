meta:
  id: cbr
  file-extension: cbr
  endian: le
seq:
  - id: header
    type: header
  - id: song_name
    type: song_name
  - id: charts
    type: charts
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
  song_name:
    seq:
      - id: song_name
        type: str
        size: 0x100
        encoding: UTF-16
  charts:
    seq:
      - id: magic
        contents: [0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: pointer
        type: u8
        repeat: expr
        repeat-expr: 4
      - id: data
        type: u8
        repeat: expr
        repeat-expr: 6
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

      - id: chart_vocals
        type: instrument
        size: pointer[3] - pointer[2]
        
      - id: chart_ending
        type: instrument
      
  instrument:
    seq:
      - id: intro
        type: u8
        repeat: expr
        repeat-expr: 4
      - id: zeros
        size: 0x1E0
      - id: head
        type: u8
        repeat: expr
        repeat-expr: 873
      - id: raw
        size-eos: true
