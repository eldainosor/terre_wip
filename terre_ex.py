#!/usr/bin/python
# Python script
# Made by Envido32

import os, shutil, subprocess
import csv
import time
import cbr, disc, band

# Config Constants 
#debug = True    #DEBUG
data_order = ("head","guitar", "rhythm", "drums", "vocals", "song")
inst_order = ("guitar", "rhythm", "drums", "vocals", "band")
diff_order = ("easy", "medium", "hard")

def copy_file(source_dir, source_file, dest_dir, dest_file):
    # Create output dir
    try:
        os.makedirs(dest_dir)
    except:
        #print("[", dest_dir, "] already exists")
        pass
    
    source = source_dir + "\\" + source_file
    dest = dest_dir + "\\" + dest_file
    try:
        print("Copying", dest_file, "...")
        shutil.copyfile(source, dest)
    except:
        print("File [", dest, "] already exists")

def promt(text, valids):
    valids_caps = []
    for valid_char in valids:
        valids_caps.append(valid_char.upper())
    input_char = ""
    while input_char not in valids_caps:
        input_char = input(str(text))[0].upper()
    return input_char

class Settings(object):
    def __init__(self, debug = False):        
        self.start_time = time.time()
        self.print_start_time()
        
        self.dir_work = os.getcwd()
        self.dir_raw = os.getcwd() + "\\raw"
        self.dir_out = os.getcwd() + "\\erdtv"

        if debug:
            print("Working dir:\t[", self.dir_work, "]")
            dir_drive = "D:"
            self.dir_mozart = dir_drive + "\\Games\\Rythm\\ERDTV\\Mozart"            
            #self.dir_mozart = self.dir_disc + "\\install\\data\\mozart"    #DEBUG
            self.convert = 'Y'            
            self.ext_videos = 'Y'
        else:
            valids = []
            for char in range(ord('A'), ord('Z')+1):
                valids.append(chr(char))
            text = "Elegi la unidad del disco de ERDTV: "
            dir_drive = promt(text, valids)
            self.dir_mozart = dir_drive + "\\install\\data\\mozart"
            valids = ['Y', 'N']
            text = "Convertir los archivos para usar en otros juegos? Esto puede tomar varios minutos: [Y/N] "
            self.convert = promt(text, valids)
            text = "Extraer videos? Esto puede tomar muchos minutos: [Y/N] "
            self.ext_videos = promt(text, valids) 
        self.dir_songs = self.dir_mozart + "\\song"
        self.dir_bands = self.dir_mozart + "\\band"
        self.dir_discs = self.dir_mozart + "\\disc"
        self.ffmpeg_file = self.dir_work + "\\ffmpeg.exe"

    def print_start_time(self):
        localtime = time.localtime(self.start_time)
        strlocal = time.strftime("%H:%M:%S", localtime)
        print("Start time:", strlocal)
        return localtime

    def print_elapsed_time(self):
        total_tm = time.time() - self.start_time
        strtotal = time.strftime("%H:%M:%S", time.gmtime(total_tm))
        print("Total time took:\t", strtotal)
        return total_tm
        
class Playlist(object):
    def __init__(self, cfg, debug = False):
        # Analize files
        print(" > Analizing files... < " )
        #os.chdir(cfg.dir_songs)
        print("Songs dir:\t[", cfg.dir_songs , "]")

        all_files = os.listdir(cfg.dir_songs)
        
        self.files = []
        for filename in all_files:
            name,ext = filename.split('.')
            if ext == "cbr":
                self.files.append(name)

        self.Songs = []

        # Create log file
        if len(self.files) > 0: #TODO move to extraction log tool
            print("Songs found in dir:\t",  len(self.files))
            #os.chdir(cfg.dir_work)
            log_file_name = "songs.csv"
            self.log_file = open(cfg.dir_work + "\\" + log_file_name, "w", newline="")
            self.log_writer = csv.writer(self.log_file)
            data_in = [ "Artista",
                        "Canción",
                        "Disco",
                        "Año",
                        "Song ID",
                        "Band ID",
                        "Disc ID",
                        "Dif:G",
                        "Dif:R",
                        "Dif:D",
                        "Dif:V",
                        "Dif:B", 
                        "Vol",
                        "Info:G",
                        "Info:R",
                        "Info:D",
                        "Info:V",
                        "Info:B",
                        #"S:G_0",
                        #"S:G_1",
                        #"S:G_2",
                        #"S:R_0",
                        #"S:R_1",
                        #"S:R_2",
                        #"S:D_0",
                        #"S:D_1",
                        #"S:D_2",
                        #"S:V_0",
                        "Res",
                        "First tick",
                        "Last tick",
                        #"BPM:cal",
            ]
            
            self.log_writer.writerow(data_in)
            self.log_file.close()

        else:
            print(" <ERROR>: No songs found in dir")

        #print("Disk dir:\t", songs_dir)    # DEBUG

    def add(self, song,  debug = False):
        self.Songs.append(song)

class Song(object):
    def __init__(self, cfg, file, debug = False):
        self.start_time = time.time()
        if debug:
            self.print_start_time()
        
        #os.chdir(cfg.dir_songs)
        self.cbr = cbr.Cbr.from_file(cfg.dir_songs + "\\" + file + ".cbr")

        # Extract metadata
        self.song_id = self.HexIDtoString(self.cbr.info.song_id)
        if debug:
            if file != self.song_id:
                print("<WARN>: File and ID does not match.")
        self.band_id = self.HexIDtoString(self.cbr.info.band_id)
        self.disc_id = self.HexIDtoString(self.cbr.info.disc_id)
        self.name = str(self.cbr.info.song_name).rstrip('\x00')
        self.year = self.cbr.info.year
        
        # Extract Difficulty
        self.diffs = self.cbr.tracks.diff_level
        band_diff = int(0)
        i = 0
        for instrument in self.cbr.tracks.diff_level:
            band_diff += instrument
            if instrument > 0:
                i += 1
        self.diffs[i] = int(band_diff / i)
        
        # Unused metadata
        self.inst_num = self.cbr.info.instr_num
        self.inst_mask = self.cbr.info.instr_mask
        self.track_info = self.cbr.tracks.trk_info[6]

        # Read band file
        #os.chdir(cfg.dir_bands)
        file_band = band.Band.from_file(cfg.dir_bands + "\\" + self.band_id + ".band")
        self.band = str(file_band.band_name).rstrip('\x00')
        
        # Read disc file
        #os.chdir(cfg.dir_discs)
        file_disc = disc.Disc.from_file(cfg.dir_discs + "\\" + self.disc_id + ".disc")
        self.disc = str(file_disc.disc_name).rstrip('\x00')

        self.dir_extr = cfg.dir_raw
        self.dir_extr += "\\"
        self.dir_extr += self.band
        self.dir_extr += " - "
        self.dir_extr += self.name

        self.dir_conv = cfg.dir_out
        self.dir_conv += "\\"
        self.dir_conv += self.band
        self.dir_conv += " - "
        self.dir_conv += self.name

        if debug:   #DEBUG
            print("Song:", self.cbr.info.song_name)  # DEBUG test Kaitai
            print("Band:", self.band)
            print("Disc:", self.disc)
            print("Year:", self.year)  # DEBUG test Kaitai
            print("Song ID:", self.song_id)  # DEBUG test Kaitai
            print("Band ID:", self.band_id)  # DEBUG test Kaitai
            print("Disc ID:", self.disc_id)  # DEBUG test Kaitai
            for i, instrument in enumerate(inst_order):
                print("Diff.", instrument ,":\t" ,self.diffs[i])  # DEBUG test Kaitai

    def extract_audio(self, cfg, debug = False):
        #os.chdir(cfg.dir_songs)

        file_au = open(cfg.dir_songs + "\\"  + self.song_id + ".au", "rb")
        song_data = file_au.read()
        flac_head = "fLaC".encode('U8')
        audio_data = song_data.split(flac_head)
        file_au.close()

        try:
            os.makedirs(self.dir_extr)
        except:
            #print("[", self.dir_extr , "] already exists")
            pass
        #os.chdir(self.dir_extr)  

        # Save steams
        for i, audio in enumerate(audio_data):
            audio_file = open(self.dir_extr + "\\" + data_order[i] + ".flac", "wb")
            audio_file.write(flac_head)
            audio_file.write(audio)
            audio_file.close()
            
    def extract_album(self, cfg, debug = False):        
        #os.chdir(cfg.dir_discs)
        file_disc = disc.Disc.from_file(cfg.dir_discs + "\\" + self.disc_id + ".disc")
        disc_img = file_disc.image.png

        try:
            os.makedirs(self.dir_extr)
        except:
            #print("[", self.dir_extr , "] already exists")
            pass
        #os.chdir(self.dir_extr)  
        
        album_file = open(self.dir_extr + "\\album.png", "wb")
        album_file.write(disc_img)
        album_file.close()
    
    def extract_background(self, cfg, debug = False):
        #os.chdir(cfg.dir_songs)
        backgnd_data = open(cfg.dir_songs + "\\" + self.song_id + ".bgf", "rb")
        backgnd_data.read(0x020C)
        backgnd_img = backgnd_data.read()
        
        try:
            os.makedirs(self.dir_extr)
        except:
            #print("[", self.dir_extr , "] already exists")
            pass
        #os.chdir(self.dir_extr)  
        
        backgnd_file = open(self.dir_extr + "\\background.png", "wb")
        backgnd_file.write(backgnd_img)
        backgnd_file.close()
    
    def extract_preview(self, cfg, debug = False):
        source_dir = cfg.dir_songs
        source_file = self.song_id + ".prv"
        dest_dir = self.dir_extr
        dest_file = "preview.wav"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def extract_video(self, cfg, debug = False):       
        source_dir = cfg.dir_songs
        source_file = self.song_id + ".vid"
        dest_dir = self.dir_extr
        dest_file = "video.asf"
        if cfg.ext_videos == 'Y':
            copy_file(source_dir, source_file, dest_dir, dest_file)
        else:
            print("Video extraction skiped")

    def extract_icon(self, cfg, debug = False):
        source_dir = cfg.dir_work
        source_file = "erdtv.png"    #TODO extract from Disk (.ico to .png)
        dest_dir = self.dir_extr
        dest_file = "erdtv.png"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def create_metadata(self, debug = False):
        try:
            os.makedirs(self.dir_extr)
        except:
            #print("[", self.dir_extr , "] already exists")
            pass
        #os.chdir(self.dir_extr)  

        ini_file = open(self.dir_extr + "\\song.ini", "w", encoding='utf-8')

        ini_file.write("[song]")
        ini_file.write("\nartist = " + self.band)
        ini_file.write("\nname = " + self.name)
        ini_file.write("\nalbum = " + self.disc)
        ini_file.write("\nyear = " + str(self.year))
        for i, instrument in enumerate(inst_order):
            ini_file.write("\ndiff_" + instrument + " = " + str(self.diffs[i]))
        ini_file.write("\nicon = " + "erdtv")
        ini_file.write("\ngenre = " + "Rock Argentino")
        ini_file.write("\ncharter = " + "Next Level")
        ini_file.write("\nbanner_link_a = " + "http://www.elrockdetuvida.com/website/index.php")
        ini_file.write("\nlink_name_a = " + "Homepage")
        ini_file.write("\nloading_phrase = " + "Viví la experiencia de interpretar los temas de tus bandas favoritas del rock nacional.")
        ini_file.write("\n;video_start_time = " + "3000")    #TODO: remove 3sec delay
        ini_file.write("\ndelay = " + "3000")                 #TODO: remove 3sec delay
        
        ini_file.close()
        
    def extract_charts(self, cfg, debug = False):
        pass    #TODO
    
    def convert_charts(self, cfg, debug = False):
        pass    #TODO

    def convert_metadata(self, debug = False):
        source_dir = self.dir_extr
        source_file = "song.ini"
        dest_dir = self.dir_conv
        dest_file = "song.ini"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def convert_album(self, debug = False):
        source_dir = self.dir_extr
        source_file = "album.png"
        dest_dir = self.dir_conv
        dest_file = "album.png"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def convert_background(self, debug = False):
        source_dir = self.dir_extr
        source_file = "background.png"
        dest_dir = self.dir_conv
        dest_file = "background.png"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def convert_icon(self, debug = False):
        source_dir = self.dir_extr
        source_file = "erdtv.png"    #TODO extract from Disk (.ico to .png)
        dest_dir = self.dir_conv
        dest_file = "erdtv.png"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def convert_audio(self, cfg, debug = False):
        pass    #TODO

    def convert_preview(self, cfg, debug = False):
        print("Compressing preview audio file with FFMPEG (WAV to OGG)")
        source_dir = self.dir_extr
        source_file = "preview.wav"
        dest_dir = self.dir_conv
        dest_file = "preview.ogg"

        try:
            cmd = cfg.ffmpeg_file 
            cmd += " -y -loglevel -8 -stats -i " 
            #cmd += cmd + " -y -stats -i "    # DEBUG Verbose 
            cmd += "\"" + source_dir + "\\" + source_file + "\""
            cmd += " -c:a libvorbis -b:a 320k " 
            cmd += "\"" +  dest_dir + "\\" + dest_file + "\""
            #print("Command:", cmd)    # DEBUG
            subprocess.run(cmd)
        except:
                print("FFMPEG.exe not found")

    def convert_video(self, cfg, debug = False):
        pass    #TODO

    def print_start_time(self):
        localtime = time.localtime(self.start_time)
        strlocal = time.strftime("%H:%M:%S", localtime)
        print("Song start:", strlocal)
        return localtime

    def print_elapsed_time(self):
        total_tm = time.time() - self.start_time
        strtotal = time.strftime("%H:%M:%S", time.gmtime(total_tm))
        print("This song took:\t", strtotal)
        return total_tm
    
    def HexIDtoString(self, hex_id):    # String formating
        str_id = str(hex(hex_id))
        str_id = str_id.upper()
        str_id = str_id.lstrip('0X')
        return str_id
