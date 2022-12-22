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
        type: flags
      - id: song_id
        type: u8
      - id: flags_2
        type: flags
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
      - id: chart_sizes
        type: chart_sizes
      - id: data1
        type: data
      - id: spacer1
        type: zeros
      - id: data2
        type: data
      - id: spacer2
        type: zeros
      - id: chart_header
        type: chart_head
      - id: spacer3
        type: zeros
      - id: chart_guitar
        type: chart_inst
      - id: rhythm_guitar
        size: 0x2320
      - id: drums_guitar
        size: 0x4910
      - id: vocals_guitar
        size: 0x4910

  chart_sizes:
    seq:
      - id: instruments
        type: u8
        repeat: expr
        repeat-expr: 5
        
  flags:
    seq:
      - id: parts
        type: u2
        repeat: expr
        repeat-expr: 4
        
  data:
    seq:
      - id: part
        type: flags
        repeat: expr
        repeat-expr: 5
        
  zeros:
    seq:
      - id: zeros
        type: u8
        repeat: until
        repeat-until: _ != 0
        
  chart_head:
    seq:
      - id: info
        type: u8
        repeat: until
        repeat-until: _ == 0

  chart_inst:
    seq:
      - id: info1
        type: u4
      - id: info2
        type: u4
      - id: magic
        contents: [0x00, 0x00, 0x00, 0x00]
