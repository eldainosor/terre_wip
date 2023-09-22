#!/usr/bin/python
# Python script
# Made by Envido32

import os, re
import csv
import time
import cbr, disc, band

# Config Constants 
#debug = True    #DEBUG
data_order = ("head","guitar", "rhythm", "drums", "vocals", "song")
inst_order = ("guitar", "rhythm", "drums", "vocals", "band")
diff_order = ("easy", "medium", "hard")

def promt(text, valids):
    valids_caps = []
    for valid_char in valids:
        valids_caps.append(valid_char.upper())
    input_char = ""
    while input_char not in valids_caps:
        input_char = input(str(text))[0].upper()
    return input_char

def HexIDtoString(hex_id):    # String formating
    str_id = str(hex(hex_id))
    str_id = str_id.upper()
    str_id = str_id.lstrip('0X')
    #aux_id = str(hex(hex_id)).upper().lstrip('0X')    # String formating
    return str_id

class Settings(object):
    def __init__(self, debug = False):        
        self.start_time = time.time()        
        
        if debug:   #DEBUG
            self.dir_drive = "D:"
            self.dir_mozart = self.dir_drive + "\\Games\\Rythm\\ERDTV\\Mozart"            
            #self.dir_mozart = self.dir_disc + "\\install\\data\\mozart"
            self.convert = 'N'            
            self.ext_videos = 'N'
        else:
            self.valids = []
            for char in range(ord('A'), ord('Z')+1):
                self.valids.append(chr(char))
            self.text = "Elegi la unidad del disco de ERDTV: "
            self.dir_drive = promt(self.text, self.valids)
            self.dir_mozart = self.dir_drive + "\\install\\data\\mozart"
            self.valids = ['Y', 'N']
            self.text = "Convertir los archivos para usar en otros juegos? Esto puede tomar varios minutos: [Y/N] "
            self.convert = promt(self.text, self.valids)
            self.text = "Extraer videos? Esto puede tomar muchos minutos: [Y/N] "
            self.ext_videos = promt(self.text, self.valids)
            del self.valids
            del self.text  
        del self.dir_drive 
        self.dir_songs = self.dir_mozart + "\\song"
        self.dir_bands = self.dir_mozart + "\\band"
        self.dir_discs = self.dir_mozart + "\\disc"
        self.dir_work = os.getcwd()
        self.dir_raw = os.getcwd() + "\\raw"
        self.dir_out = os.getcwd() + "\\erdtv"

    def print_start_time(self):
        localtime = time.localtime(self.start_time)
        strlocal = time.strftime("%H:%M:%S", localtime)
        print("Start time: ", strlocal)
        return localtime

    def print_elapsed_time(self):
        total_tm = time.time() - self.start_time
        strtotal = time.strftime("%H:%M:%S", time.gmtime(total_tm))
        print("Total time took:\t" , strtotal)
        return total_tm
        
class Playlist(object):
    def __init__(self, cfg, debug = False):
        # Analize files
        print(" > Analizing files... < " )
        os.chdir(cfg.dir_songs)
        print("Songs dir:\t[" + cfg.dir_songs  +"]")

        self.all_files = os.listdir(cfg.dir_songs)
        
        self.files = []
        for self.filename in self.all_files:
            if re.search("\.cbr$", self.filename):
                self.files.append(self.filename)
        del self.all_files

        # Create log file
        if len(self.files) > 0:
            print("Songs found in dir:\t",  len(self.files))
            os.chdir(cfg.dir_work)
            self.log_file_name = "songs.csv"
            self.log_file = open(self.log_file_name, "w", newline="")
            self.log_writer = csv.writer(self.log_file)
            self.data_in = [ "Artista",
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
            
            self.log_writer.writerow(self.data_in)
            self.log_file.close()

            del self.log_file_name
            del self.data_in            

        else:
            print("No songs found in dir")

        #print("Disk dir:\t", songs_dir)    # DEBUG

class Song(object):
    def __init__(self, cfg, file, debug = False):
        self.start_time = time.time()
        
        os.chdir(cfg.dir_songs)
        self.cbr = cbr.Cbr.from_file(file)

        # Extract Metadata
        self.song_id = HexIDtoString(self.cbr.info.song_id)
        self.band_id = HexIDtoString(self.cbr.info.band_id)
        self.disc_id = HexIDtoString(self.cbr.info.disc_id)
        self.name = str(self.cbr.info.song_name).rstrip('\x00')
        self.year = self.cbr.info.year
        
        # Extract Difficulty
        self.diffs = self.cbr.tracks.diff_level
        self.band_diff = int(0)
        i = 0
        for instrument in self.cbr.tracks.diff_level:
            self.band_diff += instrument
            if instrument > 0:
                i += 1
        self.diffs[i] = int(self.band_diff / i)
        
        self.track_info = self.cbr.tracks.trk_info[6]

        if debug:   #DEBUG
            print("Song ID = " + self.song_id)  # DEBUG test Kaitai
            print("Band ID = " + self.band_id)  # DEBUG test Kaitai
            print("Disc ID = " + self.disc_id)  # DEBUG test Kaitai
            print("Year = " + str(self.year))  # DEBUG test Kaitai
            print("Song = " + self.cbr.info.song_name)  # DEBUG test Kaitai
            for i, instrument in enumerate(inst_order):
                print("Diff. " + instrument +" =\t" + str(self.diffs[i]))  # DEBUG test Kaitai

    def print_start_time(self):
        localtime = time.localtime(self.start_time)
        strlocal = time.strftime("%H:%M:%S", localtime)
        print("Song start: ", strlocal)
        return localtime

    def print_elapsed_time(self):
        total_tm = time.time() - self.start_time
        strtotal = time.strftime("%H:%M:%S", time.gmtime(total_tm))
        print("This song took:\t", strtotal)
        return total_tm
