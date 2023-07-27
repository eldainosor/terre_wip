meta:
  id: band
  file-extension: band
  endian: le
seq:
  - id: header
    type: header
  - id: band_name
    type: str
    size: 0x7F0
    encoding: UTF-16
types:
  header:
    seq:
      - id: magic
        contents: [0x0D, 0xBA, 0x0D, 0xBA]
      - id: version
        type: u4
      - id: band_id
        type: u8 
        