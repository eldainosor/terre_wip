# Todo El Rock (Recargado)

TeRRe it’s an extraction tool for “El Rock de Tu Vida”.

[toc]

“El Rock de Tu Vida” was an Argentinian rhythm game based on the gameplay of Rock Band or Guitar Hero with licensed Argentinian music. 
Released in 2011 for Windows PC by Next Level developers and distributed by Loaded it required a permanent internet connection, since the servers were shout down the game is unplayable… until now.
All trademarks are property of their respective owners.

## Objective
Intended for archive and preservation TeRRe extracts from your LEGALY OWNED installation disc and exports it to other modern rhythm games like Clone Hero so the included songs can be played by modern audiences.

- [x] Extract songs metadata

- [x] Extract audio stems

- [x] Extract preview audio

- [x] Extract album image

- [x] Extract background image

- [x] Extract video file

- [ ] Extract instruments charts

## Requirements
TeRRe it’s a Python script and uses FFMPEG to encode audio and video. It creates an output directory with all the extracted data to be used in Clone Hero.

https://www.python.org/

https://www.ffmpeg.org/

## Usage
1) Make sure Python and FFMPEG libraries are installed on your system.
2) Run “terre.py” script.
3) Select ERDTV disc drive.
4) The extraction step should take about a minute.
5) You will be promoted if you want to encode the files (NOTE: this can take several minutes per song, be patient)
6) Once the script is done it should exit successfully

## Output
Once the script has run the following output directories should be present:
“raw”
 “[%artist name%] – [%song name%]”
  song.ini
  preview.wav
  video.asf
  background.png
  album.png
  guitar.flac
  rhythm.flac
  drums.flac
  vocals.flac
  song.flac
  charts*.cbr

“erdtv”
 “[%artist name%] – [%song name%]”
  song.ini
  preview.wav
  video.webm
  background.png
  album.png
  guitar.ogg
  rhythm. ogg
  drums. ogg
  vocals. ogg
  song.ogg
  notes*.mid

## Decription Data

[CD:/install/data/mozart/]
 [band]
  [artistID.band]
   0x0010 = Header
   0x00xx = Artist Name String
 [disc]
  [albumID.disc]
   0x0018 = Header
   0x0100 = Album Name String
   0x00xx = album.png
 [song]
  [songID.au]
   0x0000 = Header
   0x00xx = guitar.flac
   0x00xx = rhythm.flac
   0x00xx = drums.flac
   0x00xx = vocals.flac
   0x00xx = song.flac
  [songID.prv]
   preview.wav
  [songID.vid]
   video.asf
  [songID.bgf]
   0x020C = Header
   0x00xx = background.png
  [songID.cbr]
   0x001C = Header
   0x0008 = artistID (HEX Big Endian)
   0x0008 = albumID (HEX Big Endian)
   0x0004 = Album Year (int)
   0x0100 = Song Name String
   0x0A00 = Separator (2.5 KB)
   0x0600 = Chart SubHeader (8.0 KB)
   0x00xx = Guitar chart (12bits packages, 0xD007 divisor?)
   0x00xx = Chart SubHeader (8.0 KB)
   0x00xx = Rhythm chart (12bits packages, 0xD007 divisor?)
   0x00xx = Chart SubHeader (8.0 KB)
   0x00xx = Drums chart (12bits packages, 0xD007 divisor?)
   0x00xx = Chart SubHeader (8.0 KB)
   0x00xx = Vocals info (8bits packages)
   0x00xx = Vocals waves (44bits packages)
   0x00xx = Lyrics ([string][NUL]+[0xXX XX XX 00]+[0xXX XX XX 00]+[0x00 00 00 00])
   0x00xx = Engding SubHeader (8.0 KB)