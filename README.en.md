# Todo El Rock (Recargado)

TeRRe it’s an extraction tool for “El Rock de Tu Vida”.

[toc]

“El Rock de Tu Vida” was an Argentinian rhythm game based on the gameplay of Rock Band or Guitar Hero with licensed Argentinian music. 

Released in 2011 for Windows PC by Next Level developers and distributed by Loaded it required a permanent internet connection, since the servers were shout down the game is unplayable… until now.

_All trademarks are property of their respective owners._

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

- _[raw/%artist% – %song%]_: Media files extracted form the disc.

- _[erdtv/%artist% – %song%]_: Media files converted to [Clone Hero](https://clonehero.net/). NOTE: Requires [FFMPEG](https://www.ffmpeg.org/)

| raw            | erdtv          | Descripción        |
|----------------|----------------|--------------------|
| song.ini       | song.ini       | Informacion        |
| preview.wav    | preview.ogg    | Audio preliminar   |
| video.asf      | video.webm     | Video de fondo     |
| background.png | background.png | Imagen de fondo    |
| album.png      | album.png      | Tapa del disco     |
| guitar.flac    | guitar.ogg     | Audio guitarra     |
| rhythm.flac    | rhythm.ogg     | Audio bajo         |
| drums.flac     | drums.ogg      | Audio bateria      |
| vocals.flac    | vocals.ogg     | Audio cantante     |
| song.flac      | song.ogg       | Audio extras       |
| charts*.cbr    | notes*.mid     | Notas instrumentos |

## Decription Data

All song files can be found in 

- _[CD:/install/data/mozart/]_

[Kaitai Struct](https://kaitai.io/) files are avaliable for analisys

```
 [band/artistID.band]
   0x0010 = Header
   0x00xx = Artist Name String
 [disc/albumID.disc]
   0x0018 = Header
   0x0100 = Album Name String
   0x00xx = album.png
 [song/songID.au]
   0x0000 = Header
   0x00xx = guitar.flac
   0x00xx = rhythm.flac
   0x00xx = drums.flac
   0x00xx = vocals.flac
   0x00xx = song.flac
 [song/songID.prv]
   preview.wav
 [song/songID.vid]
   video.asf
 [song/songID.bgf]
   0x020C = Header
   0x00xx = background.png
 [song/songID.cbr]
   0x001C = Header
   0x0008 = artistID (HEX)
   0x0008 = albumID (HEX)
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
   0x00xx = Ending SubHeader (8.0 KB)
   ```

  
## Credits

Initial file analisis by [@eldainosor](https://twitter.com/eldainosor)

Extraction code by [@envido32](https://twitter.com/envido32)

And all the members of the awesome rhythm games comunity for their endless hard work.

_El Rock de Tu Vida, Next Level, Loaded, Rock Band, Guitar Hero, Harmonix, Activision, Clone Hero y todas las marcas y productos mencionados son propiedad de sus respectivos dueños._
