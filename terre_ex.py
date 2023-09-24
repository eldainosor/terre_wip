#!/usr/bin/python
# Python script
# Made by Envido32

import os, re, shutil
import csv, configparser
import time
import cbr, disc, band

# Config Constants 
#debug = True    #DEBUG
data_order = ("head","guitar", "rhythm", "drums", "vocals", "song")
inst_order = ("guitar", "rhythm", "drums", "vocals", "band")
diff_order = ("easy", "medium", "hard")

def copy_file(source_dir, source_file, dest_dir, dest_file):
        source = source_dir + "\\" + source_file
        dest = dest_dir + "\\" + dest_file
        name,ext = dest_file.split('.')
        if name == "erdtv":
            name = "icon"
        try:
            print("Copying", name, "...")
            shutil.copyfile(source, dest)
        except:
            print("File [ ", dest, " ] already exists")

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
            self.convert = 'N'            
            self.ext_videos = 'N'
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
        os.chdir(cfg.dir_songs)
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
            os.chdir(cfg.dir_work)
            log_file_name = "songs.csv"
            self.log_file = open(log_file_name, "w", newline="")
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
        
        os.chdir(cfg.dir_songs)
        self.cbr = cbr.Cbr.from_file(file + ".cbr")

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
        os.chdir(cfg.dir_bands)
        file_band = band.Band.from_file(self.band_id + ".band")
        self.band = str(file_band.band_name).rstrip('\x00')
        
        # Read disc file
        os.chdir(cfg.dir_discs)
        file_disc = disc.Disc.from_file(self.disc_id + ".disc")
        self.disc = str(file_disc.disc_name).rstrip('\x00')

        #self.dest_dir = cfg.dir_raw + "\\" + self.band + " - " + self.name
        self.dest_dir = cfg.dir_raw
        self.dest_dir += "\\"
        self.dest_dir += self.band
        self.dest_dir += " - "
        self.dest_dir += self.name

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
        os.chdir(cfg.dir_songs)

        file_au = open(self.song_id + ".au", "rb")
        song_data = file_au.read()
        flac_head = "fLaC".encode('U8')
        audio_data = song_data.split(flac_head)
        file_au.close()

        try:
            os.mkdir(self.dest_dir)
        except OSError as error:
            #print("[", self.dest_dir , "] already exists")
            pass
        os.chdir(self.dest_dir)  

        # Save steams
        for i, audio in enumerate(audio_data):
            new_file = open(data_order[i] + ".flac", "wb")
            new_file.write(flac_head)
            new_file.write(audio)
            new_file.close()
            
    def extract_disc_img(self, cfg, debug = False):        
        os.chdir(cfg.dir_discs)
        file_disc = disc.Disc.from_file(self.disc_id + ".disc")
        disc_img = file_disc.image.png

        try:
            os.mkdir(self.dest_dir)
        except OSError as error:
            #print("[", self.dest_dir , "] already exists")
            pass
        os.chdir(self.dest_dir)  
        
        new_file = open("album.png", "wb")
        new_file.write(disc_img)
        new_file.close()
    
    def extract_background(self, cfg, debug = False):
        os.chdir(cfg.dir_songs)
        file_bgf = open(self.song_id + ".bgf", "rb")
        file_bgf.read(0x020C)
        bgf_img = file_bgf.read()
        
        try:
            os.mkdir(self.dest_dir)
        except OSError as error:
            #print("[", self.dest_dir , "] already exists")
            pass
        os.chdir(self.dest_dir)  
        
        new_file = open("background.png", "wb")
        new_file.write(bgf_img)
        new_file.close()
    
    def extract_preview(self, cfg, debug = False):
        source_dir = cfg.dir_songs
        source_file = self.song_id + ".prv"
        dest_dir = self.dest_dir
        dest_file = "preview.wav"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def extract_video(self, cfg, debug = False):       
        source_dir = cfg.dir_songs
        source_file = self.song_id + ".vid"
        dest_dir = self.dest_dir
        dest_file = "video.asf"
        if cfg.ext_video == 'Y':
            copy_file(source_dir, source_file, dest_dir, dest_file)
        else:
            print("Video extraction skiped")

    def extract_icon(self, cfg, debug = False):
        source_dir = cfg.dir_work
        source_file = "erdtv.png"    #TODO extract from Disk (.ico to .png)
        dest_dir = self.dest_dir
        dest_file = "erdtv.png"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def create_ini(self, cfg, debug = False):
        try:
            os.mkdir(self.dest_dir)
        except OSError as error:
            #print("[", self.dest_dir , "] already exists")
            pass
        os.chdir(self.dest_dir)  
        
        config = configparser.ConfigParser()
        config.add_section("song")

        config.set("song", "artist", self.band)
        config.set("song", "name", self.name)
        config.set("song", "album", self.disc)
        config.set("song", "year", str(self.year))
        config.set("song", "diff_guitar", str(self.diffs[0]))
        config.set("song", "diff_bass", str(self.diffs[1]))
        config.set("song", "diff_drums", str(self.diffs[2]))
        config.set("song", "diff_vocals", str(self.diffs[3]))
        config.set("song", "diff_band", str(self.diffs[4]))
        config.set("song", "icon", "erdtv")
        config.set("song", "genre", "Rock Argentino")
        config.set("song", "charter", "Next Level")
        config.set("song", "banner_link_a", "http://www.elrockdetuvida.com/website/index.php")
        config.set("song", "link_name_a", "Homepage")
        config.set("song", "loading_phrase", "Viví la experiencia de interpretar los temas de tus bandas favoritas del rock nacional.")
        config.set("song", ";video_start_time" , "3000")    #TODO: remove 3sec delay
        config.set("song", "delay", "3000")                 #TODO: remove 3sec delay

        new_file = open("song.ini", "w", encoding='utf-8')
        config.write(new_file)
        new_file.close()

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
