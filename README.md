# Todo El Rock (Recargado)

**_TeRRe_** es una herramienta de extracción y preservación del juego [El Rock de Tu Vida](https://web.archive.org/web/20111020150625/http://www.elrockdetuvida.com/website/index.php) en desarrollo.

[toc]

[El Rock de Tu Vida](https://web.archive.org/web/20111020150625/http://www.elrockdetuvida.com/website/index.php) fue un juego de ritmo basado en las sagas de Rock Band o Guitar Hero con musica licenciada Argentina.

Lanzado en el año 2011 para Windows PC por los desarrolladores Next Level y distribuido por Loaded requería de una conexión permanente a internet, por lo que desde que cerraron los servidores ya no se puede jugar… hasta ahora.

Las marcas y productos mencionados son propiedad de sus respectivos dueños. 

## Objetivos

Con la intención de lograr la preservación y archivo, **_TeRRe_** extrae del disco de instalación original y exporta a otros juegos de ritmo similares (como [Clone Hero](https://clonehero.net/)) para que las canciones incluidas puedan ser disfrutadas por audiencias modernas.

- [x] Extraer la información de las canciones (metadata)

- [x] Extraer las pistas de audio de los instrumentos (stems)

- [x] Extraer el audio preliminar (preview)

- [x] Extraer la imagen de tapa del disco (album)

- [x] Extraer la imagen de fondo de los artistas (background)

- [x] Extraer el video de fondo de las canciones (video)

- [ ] Extraer las notas de los instrumentos (charts)

## Requisitos 

**_TeRRe_** esta hecho en [Python](https://www.python.org/) y utiliza [FFMPEG](https://www.ffmpeg.org/) para codificar audio y video. 

## Utilización

1) Instalar [Python](https://www.python.org/) y opcionalmente [FFMPEG](https://www.ffmpeg.org/).
2) Ejecutar el archivo _“terre.py”_
3) Seleccionar la unidad donde se encuentra el disco original de instalación.
4) La extracción debería tardar pocos minutos.
5) Si [FFMPEG](https://www.ffmpeg.org/) se encuentra instalado se puede continuar con la codificación para convertir los archivos para que sean compatibles con [Clone Hero](https://clonehero.net/). NOTA: Esto puede tardar mucho tiempo.

## Archivos de salida
Una vez finalizada la ejecución del código deberían haber dos directorios nuevos creados, cada una adentro con un directorio para cada cancion:

- _[raw/%artist% – %song%]_: Archivos audiovisuales extraídos del disco de cada una de las canciones encontradas.
- _[erdtv/%artist% – %song%]_: Archivos audiovisuales convertidos a formato compatible con [Clone Hero](https://clonehero.net/). NOTA: Requiere [FFMPEG](https://www.ffmpeg.org/)


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

## Descripción de los archivos y directorios

Todos los archivos de las canciones se encuentran en: 

- _[CD:/install/data/mozart/]_

Se han creado archivos de [Kaitai Struct](https://kaitai.io/) para el analisis de los formatos disponibles, resumidos a continuación:

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


## Créditos

Análisis inicial de los archivos por [@eldainosor](https://twitter.com/eldainosor)

Desarrollo del código de extracción [@envido32](https://twitter.com/envido32)

_El Rock de Tu Vida, Next Level, Loaded, Rock Band, Guitar Hero, Harmonix, Activision, Clone Hero y todas las marcas y productos mencionados son propiedad de sus respectivos dueños._
