#!/usr/bin/python
# Python script
# Made by Envido32

import os, re
import csv
import time

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

class Settings(object):
    def __init__(self, debug = False):        
        self.start_time = time.time()        
        
        self.localtime = time.localtime(self.start_time)
        self.local = time.strftime("%H:%M:%S", self.localtime)
        
        self.total_tm = time.time() - self.start_time
        self.total = time.strftime("%H:%M:%S", time.gmtime(self.total_tm))

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
        self.localtime = time.localtime(self.start_time)
        self.local = time.strftime("%H:%M:%S", self.localtime)
        print("Start time: ", self.local)
        return self.local

    def print_elapsed_time(self):
        self.total_tm = time.time() - self.start_time
        self.total = time.strftime("%H:%M:%S", time.gmtime(self.total_tm))
        print("Total time took:\t" , self.total)
        return self.total
        
class AnalizeDir(object):
    def __init__(self, cfg, debug = False):
        # Analize files
        print(" > Analizing files... < " )
        os.chdir(cfg.dir_songs)
        print("Songs dir:\t[" + cfg.dir_songs  +"]")

        self.dir_files = os.listdir(cfg.dir_songs)
        
        self.cbr_files = []
        for self.filename in self.dir_files:
            if re.search("\.cbr$", self.filename):
                self.cbr_files.append(self.filename)
        del self.dir_files

        # Create log file
        if len(self.cbr_files) > 0:
            print("Songs found in dir:\t",  len(self.cbr_files))
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

