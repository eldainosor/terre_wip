meta:
  id: disc
  file-extension: disc
  endian: le
seq:
  - id: header
    type: header
  - id: disc_name
    type: disc_name
  - id: image
    type: image
types:
  header:
    seq:
      - id: magic
        contents: [0x00, 0x00, 0xCC, 0xD1]
      - id: version
        type: u4
      - id: disc_id
        type: u8
      - id: band_id
        type: u8
  disc_name:
    seq:
      - id: disc_name
        type: str
        size: 0x100
        encoding: UTF-16
  image:
    seq:
      - id: magic
        contents: [0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: img_size
        type: u4
      - id: year
        type: u4
      - id: spacer
        size: 0x6D8  
      - id: png
        size: img_size