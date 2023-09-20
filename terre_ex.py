#!/usr/bin/python
# Python script
# Made by Envido32

import os
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

class Settings():
    def __init__(self, debug = False):        
        self.start_time = time.time()        
        if debug:   #DEBUG
            self.dir_disc = "D:"
            self.dir_mozart = self.dir_disc + "\\Games\\Rythm\\ERDTV\\Mozart"
            #self.dir_mozart = self.dir_disc + "\\install\\data\\mozart"
            self.convert = 'Y'
            self.ext_videos = 'N'
        else:
            self.valids = []
            for char in range(ord('A'), ord('Z')+1):
                self.valids.append(chr(char))
            self.text = "Elegi la unidad del disco de ERDTV: "
            self.dir_disc = promt(self.text, self.valids)
            self.dir_mozart = self.dir_disc + "\\install\\data\\mozart"
            self.valids = ['Y', 'N']
            self.text = "Convertir los archivos para usar en otros juegos? Esto puede tomar varios minutos: [Y/N] "
            self.convert = promt(self.text, self.valids)
            self.text = "Extraer videos? Esto puede tomar muchos minutos: [Y/N] "
            self.ext_videos = promt(self.text, self.valids)            
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

