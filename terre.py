#!/usr/bin/python
# Python script
# Made by Envido32

import os, re, shutil
import subprocess
import time

start_time = time.time()

print(" >>> EXTRACTOR TODO EL ROCK (RECARGADO) <<< ")

localtime = time.localtime(start_time)
local = time.strftime("%H:%M:%S", localtime)
print("Start time: ", local)

disc_dir = input("Elegi la unidad del disco ERDTV: ")[0].upper() + ":"
#disc_dir = "E:" # DEBUG
mozart_dir = disc_dir + "\\install\\data\\mozart"
songs_dir = mozart_dir + "\\song"
bands_dir = mozart_dir + "\\band"
albums_dir = mozart_dir + "\\disc"
work_dir = os.getcwd()
output_dir = os.getcwd() + "\\erdtv"
raw_dir = os.getcwd() + "\\raw"
data_order = ["head","guitar", "rhythm", "drums", "vocals", "song"]
 
print("Working dir:\t [", work_dir, "]")

# Analize Chart files
print(" > Analizing chart files... < " )
print("Songs dir:\t[", songs_dir ,"]")
os.chdir(songs_dir)

dir_files = os.listdir(songs_dir)
#print("Files in dir:\t",  dir_files)   #DEBUG

chart_files = list()
for filename in dir_files:
    if re.search("\.cbr$", filename):
        chart_files.append(filename)

n = len(chart_files)

# Create log file
if n > 0:
    print("Songs found in dir:\t",  n)
    os.chdir(work_dir)
    new_file = open("songs.csv", "w")
    new_file.write("Artista\tCancion\tAlbum\tAño\tSong ID\tBand ID\tAlbum ID\n")
    new_file.close()

#print("Disk dir:\t", songs_dir)    #DEBUG

# Output directories
try:
    os.mkdir(raw_dir)
except OSError as error:
    print("[", raw_dir, "] already exists")
    
# Raw extraction
for filename in chart_files:
    start_song = time.time()
    local = time.strftime("%H:%M:%S", time.localtime(start_song))
    print("Song start: ", local)

    i = chart_files.index(filename) + 1
    
    print("Analizing (", int(i) , "/" , int(n) , ")")   #DEBUG

    os.chdir(songs_dir)
    working_file = open(filename, "rb")
    song_str_id, ext = os.path.splitext(filename)

    chart_data1 = working_file.read(0x001C)

    # Extract Band ID
    band_id = bytearray(working_file.read(0x08))
    band_id.reverse()
    band_str_id = band_id.hex()
    band_str_id = band_str_id.upper()
    band_str_id = band_str_id.lstrip('0')
    
    # Extract Album ID
    album_id = bytearray(working_file.read(0x08))
    album_id.reverse()
    album_str_id = album_id.hex()
    album_str_id = album_str_id.upper()
    album_str_id = album_str_id.lstrip('0')

    # Extract Year
    year = bytearray(working_file.read(0x04))
    year.reverse()
    year_str = str(int.from_bytes(year))
    #print(year_str)    #DEBUG

    # Extract Song Name
    song_name = working_file.read(0x0100)
    song_str = song_name.decode('U16').rstrip('\0')

    # Extract Charts
    working_file.seek(0x0A00)
    chart_head = working_file.read(0x0600)
    working_file.seek(0x00)
    chart_data = working_file.read()
    charts = chart_data.split(chart_head)
    print("Charts Detected:\t", len(charts))
    working_file.close()

    print("Song ID:\t " + song_str_id)
    print("Band ID:\t " + band_str_id)
    print("Album ID:\t " + album_str_id)
    print("Song Name:\t " + song_str)
    
    # Analize Bands
    os.chdir(bands_dir)

    #dir_files = os.listdir(curr_dir) #DEBUG
    #print("Files in dir:", dir_files) #DEBUG

    working_file = open(band_str_id + ".band", "rb")
    band_data = working_file.read(0x0010)
    #print(band_data)
    band_name = working_file.read()
    band_str = band_name.decode('U16').rstrip('\0')
    print("Band Name:\t " + band_str)
    working_file.close()
    
    # Analize albums
    os.chdir(albums_dir)
    working_file = open(album_str_id + ".disc", "rb")
    album_data = working_file.read(0x0018)
    #print(album_data)
    album_name = working_file.read(0x0100)
    album_str = album_name.decode('U16').rstrip('\0')
    print("Album Name:\t " + album_str)
    album_data2 = working_file.read(0x06E8)
    album_img = working_file.read()
    working_file.close()

    # Analize Background
    os.chdir(songs_dir)
    working_file = open(song_str_id + ".bgf", "rb")
    background_data = working_file.read(0x020C)
    background_img = working_file.read()
    working_file.close()

    # Analize Stems
    #print(" > Searching band... < " )
    working_file = open(song_str_id + ".au", "rb")
    song_data = working_file.read()
    flac_head = "fLaC".encode('U8')
    audio_data = song_data.split(flac_head)
    working_file.close()

    # Output Files
    new_song_dir = raw_dir + "\\" + band_str + " - " + song_str

    try:
        os.mkdir(new_song_dir)
    except OSError as error:
        print("[", new_song_dir , "] already exists")
    os.chdir(new_song_dir)

    new_file = open("background.png", "wb")
    new_file.write(background_img)
    new_file.close()
    
    new_file = open("album.png", "wb")
    new_file.write(album_img)
    new_file.close()

    # Save steams
    for audio in audio_data:
        i = audio_data.index(audio)
        data_order[i]
        new_file = open(data_order[i] + ".flac", "wb")
        new_file.write(flac_head)
        new_file.write(audio)
        new_file.close()

    #TODO make CH compatible
    for chart in charts:
        i = charts.index(chart)
        new_file = open("chart_" + data_order[i] + ".cbr", "wb")
        if i > 0:
            new_file.write(chart_head)
        new_file.write(chart)
        new_file.close()

    # Copy preview
    source = songs_dir + "\\" + song_str_id
    dest = new_song_dir
    #print("Copying preview...")
    try:
        shutil.copyfile(source + ".prv", dest  + "\\preview.wav")
    except:
        print("File [ ", dest,  "\\preview.wav ] already exists")

    # Copy video (slow)
    #print("Copying video...")
    try:
        shutil.copyfile(source + ".vid", dest  + "\\video.asf")
    except:
        print("File [ ", dest,  "\\video.asf ] already exists")

    # Copy icon
    # TODO extract from Disk (.ico to .png)
    #print("Copying icon...")
    source = work_dir
    dest = new_song_dir
    try:
        shutil.copyfile(source + "\\erdtv.png", dest  + "\\erdtv.png")
    except:
        print("File [ ", dest,  "\\erdtv.png ] already exists")
        
    # Save metadata
    new_file = open("song.ini", "w")
    new_file.write("[song]")
    new_file.write("\nartist = " + band_str)
    new_file.write("\nname = " + song_str)
    new_file.write("\nalbum = " + album_str)
    new_file.write("\nyear = " + year_str)
    new_file.write("\nicon = erdtv")
    new_file.write("\ngenre = Rock Argentino")
    new_file.write("\ncharter = Next Level")
    new_file.write("\nbanner_link_a = http://www.elrockdetuvida.com/website/index.php")
    new_file.write("\nlink_name_a = Homepage")
    new_file.write("\nloading_phrase = Viví la experiencia de interpretar los temas de tus bandas favoritas del rock nacional.")
    new_file.write("\n;video_start_time=3000")
    new_file.write("\ndelay=3000")
    new_file.write("\n")
    new_file.close()

    # Save to log
    os.chdir(work_dir)
    new_file = open("songs.csv", "a")
    new_file.write(band_str + "\t")
    new_file.write(song_str + "\t")
    new_file.write(album_str + "\t")
    new_file.write(year_str + "\t")
    new_file.write(band_str_id + "\t")
    new_file.write(song_str_id + "\t")
    new_file.write(album_str_id + "\n")
    new_file.close()

    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_song))
    print("This song took:\t" , elapsed)
    eta_time = time.gmtime((time.time() - start_song) * (n - i))
    print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))
    
# Convert to Clone Hero (need FFMPEG)
convert = input("Convertir a Clone Hero? (esto puede tomar bastante tiempo) [y/n]: ")[0].upper()
#convert = 'Y'  #DEBUG
if convert == 'Y':
    ffmpeg_file = work_dir + "\\ffmpeg.exe"

    # Create output dir
    os.chdir(work_dir)
    try:
        os.mkdir(output_dir)
    except OSError as error:
        print("[", output_dir, "] already exists")

    # Generate lists of songs extracted
    os.chdir(raw_dir)
    songs_list = os.listdir(raw_dir)
    n = len(songs_list)

    # Loof for each song
    for this_song in songs_list:
        i = songs_list.index(this_song) + 1
        print(" >> Converting (", int(i) , "/" , int(n) , "): ", this_song) 

        start_song = time.time()
        local = time.strftime("%H:%M:%S", time.localtime(start_song))
        print("Song start: ", local)

        source_dir = raw_dir + "\\" + this_song
        dest_dir = output_dir + "\\" + this_song
        try:
            os.mkdir(dest_dir)
        except OSError as error:
            print("[", dest_dir, "] already exists")

        # Copy album image
        #print("Copying album...")
        try:
            copy_file = "\\album.png"
            source_file = source_dir + copy_file
            dest_file = dest_dir + copy_file
            shutil.copyfile(source_file, dest_file)
        except:
            print("File [ ", dest_file, " ] already exists")

        # Copy background image
        #print("Copying background...")
        try:
            copy_file = "\\background.png"
            source_file = source_dir + copy_file
            dest_file = dest_dir + copy_file
            shutil.copyfile(source_file, dest_file)
        except:
            print("File [ ", dest_file, " ] already exists")

        # Copy icon image
        #print("Copying icon...")
        try:
            copy_file = "\\erdtv.png"
            source_file = source_dir + copy_file
            dest_file = dest_dir + copy_file
            shutil.copyfile(source_file, dest_file)
        except:
            print("File [ ", dest_file, " ] already exists")

        # Copy metadata file
        #print("Copying metadata...")
        try:
            copy_file = "\\song.ini"
            source_file = source_dir + copy_file
            dest_file = dest_dir + copy_file
            shutil.copyfile(source_file, dest_file)
        except:
            print("File [ ", dest_file, " ] already exists")

        # Convert preview audio
        try:
            print("Compressing preview audio file with FFMPEG (Wav to OGG)")
            copy_file = "\\preview"
            source_file = source_dir + copy_file + ".wav"
            dest_file = dest_dir + copy_file + ".ogg"

            cmd = ffmpeg_file 
            cmd = cmd + " -y -loglevel -8 -stats -i " 
            #cmd = cmd + " -y -stats -i "    #DEBUG Verbose 
            cmd = cmd + "\"" + source_file + "\""
            cmd = cmd + " -c:a libvorbis -b:a 320k " 
            cmd = cmd + "\"" + dest_file + "\""
            subprocess.run(cmd)
        except:
            print("FFMPEG.exe not found")

        # Convert stems
        for instrument in data_order:
            try:
                print("Compressing ", instrument , " audio file with FFMPEG (Flac to OGG)")
                copy_file = "\\" + instrument
                source_file = source_dir + copy_file + ".flac"
                dest_file = dest_dir + copy_file + ".ogg"

                cmd = ffmpeg_file
                cmd = cmd + " -y -loglevel -8 -stats -i " 
                #cmd = cmd + " -y -stats -i "    #DEBUG Verbose 
                cmd = cmd + "\"" + source_file + "\""
                cmd = cmd + " -af adelay=3000:all=1 -c:a libvorbis -b:a 320k "     #Skipp 3sec
                #cmd = cmd + " -c:a libvorbis -b:a 320k " 
                cmd = cmd + "\"" + dest_file + "\""
                subprocess.run(cmd)
            except:
                print("FFMPEG.exe not found")

        # Convert video
        try:
            print("Compressing video file with FFMPEG (ASF to WEBM)")
            copy_file = "\\video"
            source_file = source_dir + copy_file + ".asf"
            dest_file = dest_dir + copy_file + ".webm"
            
            cmd = ffmpeg_file 
            #cmd = cmd + " -y -loglevel -8 -stats -ss 3000ms -i "   # Intro Skip
            cmd = cmd + " -y -loglevel -8 -stats -i "
            #cmd = cmd + " -y -stats -i "    #DEBUG Verbose 
            cmd = cmd + "\"" + source_file + "\""
            j = 0
            for instrument in data_order:
                audio_in = dest_dir + "\\" + instrument + ".ogg"
                if os.path.exists(audio_in):
                    j = j + 1
                    cmd = cmd + " -i \"" + audio_in + "\""
            cmd = cmd + " -filter_complex amix=inputs=" 
            cmd = cmd + str(int(j)) 
            cmd = cmd + ":duration=longest -c:v libvpx -crf 10 -b:v 3M -c:a libvorbis "
            cmd = cmd + "\"" + dest_file + "\""
            subprocess.run(cmd)
        except:
            print("FFMPEG.exe not found")
                    
        elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_song))
        print("This song converted in:\t" , elapsed)
        eta_time = time.gmtime((time.time() - start_song) * (n - i))
        print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))

elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
print("All tasks took: " , elapsed)