#!/usr/bin/python
# Python script

import os, re, shutil
import subprocess
import time

start_time = time.time()

print(" >>> PYTHON HEX ROCK EXTRACTOR <<< ")

localtime = time.localtime(start_time)
local = time.strftime("%H:%M:%S", localtime)
print("Start time: ", local)

disc_dir = "CD:"
mozart_dir = "\\install\\data\\mozart"
songs_dir = "\\song"
bands_dir = "\\band"
albums_dir = "\\disc"
work_dir = os.getcwd()
output_dir = os.getcwd() + "\\songs"
data_order = ["head","guitar", "rhythm", "drums", "vocals", "song"]
 
print("Working dir:\t", work_dir)
ffmpeg_file = work_dir + "\\ffmpeg.exe"

# Create log file
new_file = open("songs.csv", "w")
new_file.write("Artista\tCancion\tAlbum\tAño\tSong ID\tBand ID\tAlbum ID\n")
new_file.close()

# Analize Chart files
print(" > Analizing chart files... < " )
curr_dir = work_dir + mozart_dir + songs_dir 

print("Songs dir:\t[", curr_dir ,"]")
os.chdir(curr_dir)

dir_files = os.listdir(curr_dir)
#print("Files in dir:\t", dir_files) #DEBUG
n = len(dir_files)
n /= 5

# Output Files
try:
    os.mkdir(output_dir)
except OSError as error:
    print("[", output_dir , "] already exists")

for filename in dir_files:
    if re.search("\.cbr$", filename):
        start_song = time.time()
        local = time.strftime("%H:%M:%S", time.localtime(start_song))
        print("Song start: ", local)

        i = dir_files.index(filename)
        i /= 5
        
        print("Analizing (", int(i+1) , "/" , int(n) , ")") #DEBUG
        
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
        #print(year_str)

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
        #print(" > Searching band... < " )
        curr_dir = work_dir + mozart_dir + bands_dir 
        #print("Bands dir:\t", curr_dir)
        os.chdir(curr_dir)

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
        #print(" > Searching album... < " )
        curr_dir = work_dir + mozart_dir + albums_dir 

        #print("Album dir:\t", curr_dir)
        os.chdir(curr_dir)

        working_file = open(album_str_id + ".disc", "rb")
        album_data = working_file.read(0x0018)
        #print(band_data)
        album_name = working_file.read(0x0100)
        album_str = album_name.decode('U16').rstrip('\0')
        print("Album Name:\t " + album_str)
        album_data2 = working_file.read(0x06E8)
        album_img = working_file.read()
        working_file.close()

        # Analize Background
        #print(" > Analizing backgrounds... < " )
        curr_dir = work_dir + mozart_dir + songs_dir 
        #print("Songs dir:\t", curr_dir)
        os.chdir(curr_dir)

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
        #song_head, guitar, rhythm, drums, vocals, song = song_data.split(flac_head)
        working_file.close()

        # Output Files
        new_song_dir = output_dir + "\\" + band_str + " - " + song_str
        try:
            os.mkdir(new_song_dir)
        except OSError as error:
            #continue
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
            try:
                print("Compressing ", data_order[i] , " audio file with FFMPEG (Flac to OGG)")
                cmd = ffmpeg_file + " -y -loglevel -8 -stats -i " + data_order[i] + ".flac -af adelay=3000:all=1 -c:a libvorbis -b:a 320k " + data_order[i] + ".ogg"
                subprocess.run(cmd)
                os.remove(new_song_dir + "\\" + data_order[i] + ".flac")
            except:
                print("FFMPEG.exe not found")
        try:
            os.remove(new_song_dir + "\\head.flac")
        except:
            print("No head.flac")

        for chart in charts:
            i = charts.index(chart)
            new_file = open("chart_" + data_order[i] + ".cbr", "wb")
            if i != 0:
                new_file.write(chart_head)
            new_file.write(chart)
            new_file.close()
            #TODO make CH compatible

        # Copy preview
        source = work_dir + mozart_dir + songs_dir + "\\" + song_str_id
        dest = new_song_dir
        #print("Copying preview...")
        shutil.copy(source + ".prv", dest  + "\\preview.wav")
        try:
            print("Compressing preview audio file with FFMPEG (Wav to OGG)")
            cmd = ffmpeg_file + " -y -loglevel -8 -stats -i preview.wav -c:a libvorbis -b:a 320k preview.ogg"
            subprocess.run(cmd)
            os.remove(new_song_dir + "\\preview.wav")
        except:
                print("FFMPEG.exe not found")

        # Copy video (slow)
        #print("Copying video...")
        shutil.copy(source + ".vid", dest  + "\\video.asf")

        try:
            print("Compressing video file with FFMPEG (ASF to WEBM)")

            cmd = ffmpeg_file + " -y -loglevel -8 -stats -i video.asf " 
            #cmd = ffmpeg_file + " -y -stats -i video.asf " 
            j = 0
            for audio_in in data_order:
                dir_test = new_song_dir + "\\" + audio_in + ".ogg"
                if os.path.exists(dir_test):
                    j = j + 1
                    cmd = cmd + "-i " + audio_in + ".ogg "
            #cmd = cmd + "-filter_complex amix=inputs=" + str(int(j)) + ":duration=longest[0];[0]adelay=3000:all=1 -c:v libvpx -crf 10 -b:v 3M -c:a libvorbis video.webm"
            cmd = cmd + "-filter_complex amix=inputs=" + str(int(j)) + ":duration=longest -c:v libvpx -crf 10 -b:v 3M -c:a libvorbis video.webm"
            subprocess.run(cmd)
            os.remove(new_song_dir + "\\video.asf")
        except:
            print("FFMPEG.exe not found")

        # Copy icon
        # TODO extract from CD
        source = work_dir
        dest = new_song_dir
        #print("Copying icon...")
        shutil.copy(source + "\\erdtv.png", dest  + "\\erdtv.png")
        
        # Save info
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

        # Back to mozart
        curr_dir = work_dir + mozart_dir + songs_dir 
        os.chdir(curr_dir)

        elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_song))
        print("Song tasks took: " , elapsed)

elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
print("All tasks took: " , elapsed)