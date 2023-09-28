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

def copy_file(source_dir:str, source_file:str, dest_dir:str, dest_file:str):
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

def promt(text:str, valids:str):
    valids_caps = []
    for valid_char in valids:
        valids_caps.append(valid_char.upper())
    input_char = ""
    while input_char not in valids_caps:
        input_char = input(str(text))[0].upper()
    return input_char

def dicts_to_csv(file:str, dict:dict, debug = False):
    keys = list(dict[0].keys())
    csv_line = ""
    for col in keys:
        csv_line += col
        csv_line += ","
    csv_line += "\n"

    new_csv = open(file, "w", encoding='utf-8')
    new_csv.write(csv_line)

    for this_dict in dict:
        csv_line = ""
        for col in keys:
            csv_line += str(this_dict[col])
            csv_line += ","
        csv_line += "\n"
        new_csv.write(str(csv_line))
    new_csv.close()

class Settings(object):
    def __init__(self, debug = False):        
        self.start_time = time.time()
        self.print_start_time()
        
        self.dir_work = os.getcwd()
        self.dir_raw = self.dir_work + "\\raw"
        self.dir_out = self.dir_work + "\\erdtv"

        if debug:
            print("Working dir:\t[", self.dir_work, "]")
            dir_drive = "D:"
            self.dir_mozart = dir_drive + "\\Games\\Rythm\\ERDTV\\Mozart"            
            #self.dir_mozart = self.dir_disc + "\\install\\data\\mozart"    #DEBUG
            self.convert = 'Y'            
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
        
class Song(object):
    def __init__(self, cfg:Settings, file:str, debug = False):
        self.start_time = time.time()
        if debug:
            self.print_start_time()
        
        kaitai = cfg.dir_songs
        kaitai += "\\"
        kaitai += file
        kaitai += ".cbr"
        self.cbr = cbr.Cbr.from_file(kaitai)  #TODO: Delete when Methons are is done
        chart_band_record = cbr.Cbr.from_file(kaitai)

        # Extract metadata
        self.song_id = self.HexIDtoString(chart_band_record.song_id)
        if debug:
            if file != self.song_id:
                print("<WARN>: File and ID are diferent")
        self.band_id = self.HexIDtoString(chart_band_record.band_id)
        self.disc_id = self.HexIDtoString(chart_band_record.disc_id)
        self.name = str(chart_band_record.song_name).rstrip('\x00')
        self.year = chart_band_record.year
        
        # Extract Difficulty Level
        self.diffs = []
        band_diff = int(0)
        i = 0
        for instrument in chart_band_record.diff_level:
            if instrument > 0:
                band_diff += instrument
                self.diffs.append(instrument)
                i += 1
            #else:
            #    print("<WARN>: Diff is ZERO")
        self.diffs.append(int(band_diff / i))
        
        # Unused metadata
        self.inst_num = chart_band_record.instr_num
        self.inst_mask = chart_band_record.instr_mask
        self.track_info = int.from_bytes(chart_band_record.meta_end)

        # Read band file
        kaitai = cfg.dir_bands
        kaitai += "\\"
        kaitai += self.band_id
        kaitai += ".band"
        file_band = band.Band.from_file(kaitai)
        self.band = str(file_band.band_name).rstrip('\x00')
        
        # Read disc file
        kaitai = cfg.dir_discs
        kaitai += "\\"
        kaitai += self.disc_id
        kaitai += ".disc"
        file_disc = disc.Disc.from_file(kaitai)
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
            print("Song:", self.name)  # DEBUG test Kaitai
            print("Band:", self.band)
            print("Disc:", self.disc)
            print("Year:", self.year)  # DEBUG test Kaitai
            print("Song ID:", self.song_id)  # DEBUG test Kaitai
            print("Band ID:", self.band_id)  # DEBUG test Kaitai
            print("Disc ID:", self.disc_id)  # DEBUG test Kaitai
            for i, instrument in enumerate(inst_order):
                print("Diff.", instrument ,":\t" ,self.diffs[i])  # DEBUG test Kaitai

    def extract_audio(self, cfg:Settings, debug = False):
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

        # Save steams
        for i, audio in enumerate(audio_data):
            audio_file = open(self.dir_extr + "\\" + data_order[i] + ".flac", "wb")
            audio_file.write(flac_head)
            audio_file.write(audio)
            audio_file.close()
            
    def extract_album(self, cfg:Settings, debug = False):
        kaitai = cfg.dir_discs
        kaitai += "\\"
        kaitai += self.disc_id
        kaitai += ".disc"
        file_disc = disc.Disc.from_file(kaitai)
        disc_img = file_disc.image.png

        try:
            os.makedirs(self.dir_extr)
        except:
            #print("[", self.dir_extr , "] already exists")
            pass
        
        album_file = open(self.dir_extr + "\\album.png", "wb")
        album_file.write(disc_img)
        album_file.close()
    
    def extract_background(self, cfg:Settings, debug = False):
        backgnd_data = open(cfg.dir_songs + "\\" + self.song_id + ".bgf", "rb")
        backgnd_data.read(0x020C)
        backgnd_img = backgnd_data.read()
        
        try:
            os.makedirs(self.dir_extr)
        except:
            #print("[", self.dir_extr , "] already exists")
            pass
        
        backgnd_file = open(self.dir_extr + "\\background.png", "wb")
        backgnd_file.write(backgnd_img)
        backgnd_file.close()
    
    def extract_preview(self, cfg:Settings, debug = False):
        source_dir = cfg.dir_songs
        source_file = self.song_id + ".prv"
        dest_dir = self.dir_extr
        dest_file = "preview.wav"
        copy_file(source_dir, source_file, dest_dir, dest_file)

    def extract_video(self, cfg:Settings, debug = False):       
        source_dir = cfg.dir_songs
        source_file = self.song_id + ".vid"
        dest_dir = self.dir_extr
        dest_file = "video.asf"
        if cfg.ext_videos == 'Y':
            copy_file(source_dir, source_file, dest_dir, dest_file)
        else:
            print("Video extraction skiped")

    def extract_icon(self, cfg:Settings, debug = False):
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
        ini_file.write("\ndelay = " + "3000")                #TODO: remove 3sec delay
        
        ini_file.close()
        
    def extract_charts(self, cfg:Settings, debug = False):
        self.Tracks = []
        kaitai = cfg.dir_songs
        kaitai += "\\"
        kaitai += self.song_id
        kaitai += ".cbr"
        chart_band_record = cbr.Cbr.from_file(kaitai)
        for inst_raw in chart_band_record.charts:
            inst_clean = Track(inst_raw, debug)
            self.Tracks.append(inst_clean)

        '''
        if debug:
            test_pulse = self.Tracks[0].pulse
            for this_track in self.Tracks:
                for i in test_pulse:
                    if i not in this_track.pulse:
                        print("<WARN>: Pulses not match", i)
        '''

        for this_track in self.Tracks:
            this_track.extract(self.dir_extr, debug)
            
    def convert_charts(self, cfg:Settings, debug = False):
        #TODO: from CSV to CHART using self.Tracks
        source_dir = self.dir_extr
        source_file = "notes.chart"
        dest_dir = self.dir_conv
        dest_file = "notes.chart"
        copy_file(source_dir, source_file, dest_dir, dest_file)

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

    def convert_audio(self, cfg:Settings, debug = False):
        for instrument in data_order:
            print("Compressing", instrument, "audio file with FFMPEG (Flac to OGG)")
            source_dir = self.dir_extr
            source_file = instrument + ".flac"
            dest_dir = self.dir_conv
            dest_file =  instrument + ".ogg"

            try:
                cmd = cfg.ffmpeg_file 
                cmd += " -y -loglevel -8 -stats -i " 
                #cmd += cmd + " -y -stats -i "    # DEBUG Verbose 
                cmd += "\"" + source_dir + "\\" + source_file + "\""
                cmd += " -af adelay=3000:all=1 -c:a libvorbis -b:a 320k "      #Skipp 3sec #TODO: remove 3sec delay
                #cmd += " -c:a libvorbis -b:a 320k "                           #Skipp 3sec #TODO: remove 3sec delay
                cmd += "\"" +  dest_dir + "\\" + dest_file + "\""
                #print("Command:", cmd)    # DEBUG
                subprocess.run(cmd)
            except:
                print("FFMPEG.exe not found")

    def convert_preview(self, cfg:Settings, debug = False):
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

    def convert_video(self, cfg:Settings, debug = False):
        print("Compressing video file with FFMPEG (ASF to WEBM)")
        source_dir = self.dir_extr
        source_file = "video.asf"
        dest_dir = self.dir_conv
        dest_file = "video.webm"

        try:
            cmd = cfg.ffmpeg_file 
            cmd += " -y -loglevel -8 -stats -hwaccel auto -i "
            cmd += "\"" + source_dir + "\\" + source_file + "\""
            for i, instrument in enumerate(data_order):
                audio_in = dest_dir + "\\" + instrument + ".ogg"
                if os.path.exists(audio_in):
                    cmd += " -i \"" + audio_in + "\""
            #cmd += " -ss 3000ms -filter_complex amix=inputs="     # Intro Skip #TODO: remove 3sec delay
            cmd += " -filter_complex amix=inputs="                 # Intro Skip #TODO: remove 3sec delay
            cmd += str(int(i)) 
            cmd += ":duration=longest -c:v libvpx -quality good -crf 12 -b:v 2000K -map 0:v:0? -an -sn -map_chapters -1 -f webm "
            cmd += "\"" +  dest_dir + "\\" + dest_file + "\""
            #print("Command: " + cmd)    # DEBUG
            subprocess.run(cmd)
        except:
            print("FFMPEG.exe not found")

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

class Playlist(object):
    def __init__(self, cfg:Settings, debug = False):
        # Analize files
        print(" > Analizing files... < " )
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

    def append(self, song:Song,  debug = False):
        self.Songs.append(song)

class Track(object):
    def __init__(self, cbr_chart:cbr.Cbr.Charts, debug = False):
        self.id_num = cbr_chart.inst_id.value
        self.name = cbr_chart.inst_id.name
        self.info = int.from_bytes(cbr_chart.chart_info)   #Unknown usage
        unsorted_pulse = []
        for this_pulse in cbr_chart.pulse:
            pulse_dict = {
                "time": this_pulse.time,
                "type": this_pulse.type
            }
            unsorted_pulse.append(pulse_dict)
        self.pulse = sorted(unsorted_pulse, key=lambda item: item['time'])
        
        if self.id_num < 3:
            self.Diffs = []
            for diff_raw in cbr_chart.inst.diff_charts:
                diff_clean = Chart(diff_raw, debug)
                self.Diffs.append(diff_clean)

        if self.name == "vocals":
            self.Lyrics = Lyrics(cbr_chart.vocals, debug)

    def extract(self, dir_extr:str, debug = False):
        file = dir_extr
        file += "\\"
        file += self.name
        file += "_"
        file += "pulse"
        file += "-"
        file += str(self.info)
        file += ".csv"
        dicts_to_csv(file, self.pulse)

        if self.id_num < 3:
            for this_diff in self.Diffs:
                this_dir = dir_extr
                this_dir += "\\"
                this_dir += self.name
                this_diff.extract(this_dir, debug)
        
        if self.name == "vocals":
            this_dir = dir_extr
            this_dir += "\\"
            this_dir += self.name
            self.Lyrics.extract(dir_extr, debug)     

class Chart(object):
    def __init__(self, cbr_diff:cbr.Cbr.Instrument, debug = False):
        self.id_num = cbr_diff.diff.value
        self.name = cbr_diff.diff.name
        self.info = cbr_diff.diff_info  #Unknown usage

        self.max_note = cbr_diff.num_frets_pts
        if debug:
            if self.max_note != 5:  #DEBUG
                print("<WARN>: Frets number is", self.max_note)
        unsorted_notes = []

        for i, this_color in enumerate(cbr_diff.frets_on_fire):
            for this_note in this_color.frets_wave:
                note_dict = {
                    "time": this_note.time,
                    "len": this_note.len,
                    "note": i,
                    "mods": this_note.mods
                }
                unsorted_notes.append(note_dict)
        self.notes = sorted(unsorted_notes, key=lambda item: item['time'])
 
    def extract(self, dir_extr, debug = False):
        file = dir_extr
        file += "_"
        file += self.name
        file += "-"
        file += str(self.info)
        file += ".csv"
        dicts_to_csv(file, self.notes)

class Lyrics(object):
    def __init__(self, cbr_vocal:cbr.Cbr.Voice, debug = False):
        unsorted_pitch = []
        unsorted_harm = []
        unsorted_verses = []
        self.info = int.from_bytes(cbr_vocal.vocal_info)  #Unknown usage

        for verse_raw in cbr_vocal.lyrics:
            verse_clean = Verse(verse_raw, debug)
            unsorted_verses.append(verse_clean)
        
        for this_wave in cbr_vocal.wave_form:
            pitch_dict = {
                "time": this_wave.start,
                "len": (this_wave.end - this_wave.start),
                "note": this_wave.note,
                "mods": this_wave.mod,
                "scale": this_wave.scale,
            }

            harm_dict = {
                "time": this_wave.start_harm,
                "len": (this_wave.end_harm - this_wave.start_harm),
                "note": this_wave.note_harm,
                "mods": this_wave.mod,
                "scale": this_wave.scale,
            }

            if debug:
                if pitch_dict != harm_dict:
                    print("<WARN>: Pitch and Harm are diferent")

            unsorted_pitch.append(pitch_dict)
            unsorted_harm.append(harm_dict)

        self.verses = sorted(unsorted_verses, key=lambda item: item.time)
        self.pitch = sorted(unsorted_harm, key=lambda item: item['time'])
        self.harm = sorted(unsorted_harm, key=lambda item: item['time'])

    def extract(self, dir_extr:str, debug = False):
        file = dir_extr
        file += "\\"
        file += "vocals"
        file += "_"
        file += "pitch"
        file += "-"
        file += str(self.info)
        file += ".csv"
        dicts_to_csv(file, self.pitch)
        
        file = dir_extr
        file += "\\"
        file += "vocals"
        file += "_"
        file += "harm"
        file += "-"
        file += str(self.info)
        file += ".csv"
        dicts_to_csv(file, self.harm)

        file = dir_extr
        file += "\\"
        file += "vocals"
        file += "_"
        file += "lyrics"    
        file += "-"
        file += str(self.info)
        file += ".lrc"
        
        lrc_file = open(file, "w", encoding='utf-8')

        #lrc_file.write("[ar: " + self.band + "]\n")
        #lrc_file.write("[al: " + self.disc + "]\n")
        #lrc_file.write("[ty: " + self.name + "]\n")

        for this_verse in self.verses:
            lrc_file.write("\n[" + str(this_verse.time) + "]")
            for this_syll in this_verse.syllables:
                lrc_file.write(" <" + str(this_syll['time']) + "> " + str(this_syll['note']))
            this_verse.extract(file, debug)

        lrc_file.close()

class Verse(object):
    def __init__(self, cbr_verse:cbr.Cbr.Verse, debug = False):
        self.time = cbr_verse.time_start
        self.mods = cbr_verse.mods
        self.len = cbr_verse.time_end - cbr_verse.time_start
        
        dur_sum = 0
        unsorted_syll = []
        for this_syll in cbr_verse.text_block:
            syll_dict = {
                "time": this_syll.time_start,
                "len": (this_syll.time_end - this_syll.time_start),
                "note": this_syll.text,
                "mods": this_syll.type
            }
            dur_sum += syll_dict["len"]
            unsorted_syll.append(syll_dict)
        self.syllables = sorted(unsorted_syll, key=lambda item: item['time'])

        if debug:
            if dur_sum != cbr_verse.len:
                print("<WARN>: Dur and Len are diferent")

    def extract(self, dir_extr:str, debug = False):
        file = dir_extr
        file += "\\"
        file += str(self.time)
        file += ".csv"
        #dicts_to_csv(file, self.syllables)
            