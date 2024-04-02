#!/usr/bin/python
# Python script
# Made by Envido32

import os, shutil, subprocess
import time
import cbr, disc, band
from ter_conv import *
from midiutil.MidiFile import MIDIFile
import math
#from itertools import zip_longest

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

    csv_new = open(file, "w", encoding='utf-8')
    csv_new.write(csv_line)

    for this_dict in dict:
        csv_line = ""
        for col in keys:
            csv_line += str(this_dict[col])
            csv_line += ","
        csv_line += "\n"
        csv_new.write(csv_line)
    csv_new.close()

def ticks_to_clock(ticks:int, rate:int):
    secs = ticks / rate
    min = int(secs // 60)
    sec = int(secs % 60)
    dec = int((secs % 1) * 100)
    clock = f"{min:02d}:{sec:02d}.{dec:02d}"
    return clock

class Settings(object):
    def __init__(self, debug = False):        
        self.start_time = time.time()
        self.print_start_time()
        
        self.dir_work = os.getcwd()
        self.dir_raw = self.dir_work + "\\raw"
        self.dir_out = self.dir_work + "\\erdtv"

        if debug:
            print("Working dir:\t[", self.dir_work, "]")
            #dir_drive = "D:"
            #self.dir_mozart = dir_drive + "\\Games\\Rythm\\ERDTV\\Mozart"            
            self.dir_mozart = self.dir_work + "\\..\\..\\Mozart"  
            self.convert = 'Y'
            self.ext_videos = 'Y'
        else:
            valids = []
            for char in range(ord('A'), ord('Z')+1):
                valids.append(chr(char))
            text = "Elegi la unidad del disco de ERDTV: "
            dir_drive = promt(text, valids)
            self.dir_mozart = dir_drive + ":\\INSTALL\\DATA\\MOZART"
            valids = ['Y', 'N']
            text = "Convertir los archivos para usar en otros juegos? Esto puede tomar varios minutos: [Y/N] "
            self.convert = promt(text, valids)
            text = "Extraer videos? Esto puede tomar muchos minutos: [Y/N] "
            self.ext_videos = promt(text, valids) 
        self.dir_songs = self.dir_mozart + "\\SONG"
        self.dir_bands = self.dir_mozart + "\\BAND"
        self.dir_discs = self.dir_mozart + "\\DISC"
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
        self.cbr = cbr.Cbr.from_file(kaitai)  #TODO: Delete when Methods are done
        chart_band_record = cbr.Cbr.from_file(kaitai)

        # Extract metadata
        self.song_id = self.HexIDtoString(chart_band_record.song_id)
        if debug:
            if file != self.song_id:
                print("<WARN>: File and ID are diferent")
        self.band_id = self.HexIDtoString(chart_band_record.band_id)
        self.disc_id = self.HexIDtoString(chart_band_record.disc_id)
        self.name = str(chart_band_record.song_name).rstrip('\x00')
        self.year = int(chart_band_record.year)
        
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
        self.delay = 3000   #TODO: remove 3sec delay
        #self.delay = 0.0   #TODO: remove 3sec delay

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

        log_file = open(cfg.log_file, "a", newline="")

        log_line = ""
        log_line += "\"" + self.band + "\","
        log_line += "\"" + self.name + "\","
        log_line += "\"" + self.disc + "\","
        log_line += str(self.year) + ","
        log_line += self.song_id + ","
        log_line += self.band_id + ","
        log_line += self.disc_id + ","
        for i, instrument in enumerate(inst_order):
            log_line += str(self.diffs[i]) + ","
        log_line += "\n"
            
        log_file.write(log_line)
        log_file.close()

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
        print("Creating song.ini ...")

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
        ini_file.write("\n;video_start_time = " + str(int(self.delay)))    #TODO: remove 3sec delay
        ini_file.write("\ndelay = " + str(int(self.delay)))                #TODO: remove 3sec delay
        
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
        for this_track in self.Tracks:
            this_track.extract(self, debug)

        '''
        if debug:
            self.test_unify_pulses(debug)
        
    def test_unify_pulses(self, debug = False):
        file = self.dir_extr
        file += "\\"
        file += "pulse"
        file += "_"
        file += "all"
        file += ".csv"
        lines_all = []
        for this_track in self.Tracks:
            #print("Pulse len for", this_track.name, ":",len(this_track.pulse))
            keys = list(this_track.pulse[0].keys())
            for this_key in keys:
                csv_line = [ this_key ] 
                for this_pulse in this_track.pulse:
                    csv_line.append(this_pulse[this_key])
                lines_all.append(csv_line)

        trans_data = list(zip_longest(*lines_all, fillvalue=''))
        
        csv_new = open(file, "w", encoding='utf-8')
        for this_line in trans_data:
            csv_line = ""
            for this_data in this_line:
                csv_line += str(this_data)
                csv_line += ','
            csv_line += '\n'
            csv_new.write(csv_line)
        csv_new.close()
        '''
            
    def convert_charts(self, cfg:Settings, debug = False):
        print("Creating notes.mid ...")
        self.chart_file = self.dir_conv
        self.chart_file += "\\"
        self.chart_file += "notes.mid"

        global chartMidiFile
        chartMidiFile = MIDIFile(4, eventtime_is_ticks=True, ticks_per_quarternote=480, deinterleave=False)
        
        inst_pulse = self.Tracks[2].pulse
        bmp_data, res, delay = analize_pulse(inst_pulse, debug)
        self.delay += delay

        self.save_charts_meta(res, debug)
        self.charts_sync_track(bmp_data, debug)
        self.charts_lyrics(bmp_data, debug)
        self.charts_inst(bmp_data, debug)

        with open(self.chart_file, 'wb') as outf:
            chartMidiFile.writeFile(outf)
        '''
        if debug:
            #self.charts_pulse(bmp_data, inst_pulse, debug)
        '''

    def save_charts_meta(self, res:int, debug = False):
        try:
            os.makedirs(self.dir_conv)
        except:
            #print("[", self.dir_conv , "] already exists")
            pass

    def charts_sync_track(self, bmp_data:dict, debug = False):
        # chart_file = open(self.chart_file, "a", encoding='utf-8')
        # chart_file.write("[SyncTrack]")
        # chart_file.write("\n{")
        for data in bmp_data:
            match str(data['type']):
                case "TS":
                    # TODO: Parse in case there's more than 2 values
                    numerTS = int(data['value'])
                    denomTS = 2
                    if (int(data['value']) == 1):
                        denomTS = 1
                    else:
                        denomTS = int(int(data['value']) / 2)
                    chartMidiFile.addTimeSignature(0, int(data['tick']), numerTS, denomTS, 24)
                case "B":
                    this_tempo_change = int(int(data['value']) / 1000)
                    chartMidiFile.addTempo(0, int(data['time']), this_tempo_change)
            
            line_data = "\n  "
            #line_data += str(data['time'])
            line_data += str(data['tick'])
            line_data += " = "
            line_data += str(data['type'])
            line_data += " "
            line_data += str(data['value'])
            #line_data += "\t"
            #line_data += str(data['tick'])
            # chart_file.write(line_data)
        # chart_file.write("\n}\n")
        # chart_file.close()


    '''
    def charts_pulse(self, bmp_data:dict, inst_pulse:dict, debug = False):
        #TODO: Convert all 'time' to 'tick' with BPMs
        # chart_file =open(self.chart_file, "a", encoding='utf-8')

        # chart_file.write("[ExpertDrums]")
        # chart_file.write("\n{")

        notes_list = []
        for this_pulse in inst_pulse:
            #aux = 3 - this_pulse['type']
            aux = this_pulse['type'] + 1
            #aux += 2
            #aux %= 4
            note_in = {
                "time":     int(this_pulse['time']),
                "type":     "N " + str(int(aux)),
                "value":    int(0)
            }
            notes_list.append(note_in)
        notes_list = sorted(notes_list, key=lambda item: item['time'])
        #sorted_notes = sorted(notes_list, key=lambda item: item[0])

        for data in notes_list:
            line_data = "\n  "
            line_data += str(data['time'])
            line_data += " = "
            line_data += str(data['type'])
            line_data += " "
            line_data += str(data['value'])
            # chart_file.write(line_data)
        # chart_file.write("\n}\n")
        # chart_file.close()
    '''

    def charts_lyrics(self, bpm_data:dict, debug = False):
        chartMidiFile.addTrackName(3, 0, "PART VOCALS")
        for this_phrase in self.Tracks[3].Lyrics.verses:
            tick_start_time = int(SwapTimeForDis(this_phrase.time, bpm_data))
            tick_end_time = int(SwapTimeForDis(this_phrase.time + this_phrase.len, bpm_data))
            tick_full_length = tick_end_time - tick_start_time
            chartMidiFile.addNote(3, 0, 105, tick_start_time, tick_full_length, 100)
            #event_line += str(this_phrase.time)
            countSyll = 0
            for this_syll in this_phrase.syllables:
                this_tick = SwapTimeForDis(this_syll['time'], bpm_data)
                this_tick_length = SwapTimeForDis(this_syll['len'], bpm_data)

                # THIS IS SO UGLY
                this_tick_note = 0
                this_tick_scale = 0
                prev_tick_scale = 0
                this_tick_has_mod = 0
                for currentPitch in self.Tracks[3].Lyrics.pitch:
                    if this_syll['time'] == currentPitch['time']:
                        this_tick_note = currentPitch['note']
                        this_tick_scale = currentPitch['scale']
                        this_tick_has_mod = currentPitch['mods']   

                #bruh this hack is to see if we can make it higher or lower
                final_tick_pitch = 36
                if countSyll > 0:
                    if this_tick_scale > prev_tick_scale:
                        # verify that the diff is higher
                        if (this_tick_scale - prev_tick_scale) > 2:
                            final_tick_pitch = final_tick_pitch + 12
                        elif int(this_tick_note) == 0:
                            this_tick_note = 12
                    elif this_tick_scale < prev_tick_scale:
                        # verify that the diff is higher
                        if (prev_tick_scale - this_tick_scale) > 2:
                            final_tick_pitch = final_tick_pitch - 12
                        elif int(this_tick_note) == 0:
                            this_tick_note = 12

                this_tick_pitch = (final_tick_pitch) + int(this_tick_note)

                #this_tick_pitch = (36 + (12*3))
                #event_line += str(this_syll['time'])
                chartMidiFile.addNote(3, 0, this_tick_pitch, int(this_tick), int(this_tick_length), 100)

                chartMidiFile.addText(3, int(this_tick), str(this_syll['note']))

                ## HACKY WAY TO IMPLEMENT LYRICS MODULATION
                if this_tick_has_mod == 1:
                    chartMidiFile.addText(3, int(this_tick) + int(this_tick_length) + 20, " + ")
                # chart_file.write(event_line)
                countSyll = countSyll + 1
                prev_tick_scale = this_tick_scale
            

    def charts_inst(self, bmp_data:dict, debug = False):
        # chart_file =open(self.chart_file, "a", encoding='utf-8')
        this_inst_track = -1
        for this_inst in self.Tracks:
            if this_inst.id_num < 3:
                this_inst_name = this_inst.name
                match this_inst_name:
                    case "guitar":
                        this_inst_track = 0
                        chartMidiFile.addTrackName(this_inst_track, 0, "PART GUITAR")
                    case "rhythm":
                        this_inst_track = 1
                        chartMidiFile.addTrackName(this_inst_track, 0, "PART BASS")
                    case "drums":
                        this_inst_track = 2
                        chartMidiFile.addTrackName(this_inst_track, 0, "PART DRUMS")
                    case _:
                        this_inst_track = -1
                        this_inst_name = ""
            
                for this_diff in reversed(this_inst.Diffs):
                    this_diff_name = this_diff.name
                    # chart_file.write("[" + this_diff_name.capitalize() + this_inst_name + "]")
                    # chart_file.write("\n{")

                    # Setting this to expert by default (won't be used)
                    diff_note_base = 96
                    match this_diff_name:
                        case "easy":
                            diff_note_base = 60
                        case "medium":
                            diff_note_base = 72
                        case "hard":
                            diff_note_base = 84
                        case _:
                            diff_note_base = 96

                    chart_data = analize_charts(this_diff.notes, bmp_data, debug)
                    for data in chart_data:
                        line_data = "\n  "
                        #line_data += str(data['time'])
                        line_data += str(data['tick'])
                        line_data += " = "
                        line_data += str(data['type'])
                        line_data += " "
                        line_data += str(data['len'])
                        if str(data['type']) == "S 2":
                            chartMidiFile.addNote(this_inst_track, 0, 116, int(data['tick']), data['len'], 100)
                        else:
                            #final_note_length = data['len'] == 0 ? 100 : data['len']
                            final_note_length = 100 if data['len'] == 0 else data['len']
                            chartMidiFile.addNote(this_inst_track, 0, diff_note_base + int(data['type'][2:]), int(data['tick']), final_note_length, 100)
                        '''
                        line_data += "\t"
                        line_data += str(data['value'])
                        line_data += "\t"
                        line_data += str(data['time'])
                        '''
                        # chart_file.write(line_data)
                    # chart_file.write("\n}\n")
        # chart_file.close()

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

            #TODO: use Python FFMPEG or ask for download
            try:
                cmd = cfg.ffmpeg_file 
                cmd += " -y -loglevel -8 -stats -i " 
                #cmd += cmd + " -y -stats -i "    # DEBUG Verbose 
                cmd += "\"" + source_dir + "\\" + source_file + "\""
                cmd += " -af adelay=" + str(self.delay) + ":all=1 -c:a libvorbis -b:a 320k "      #Skipp 3sec #TODO: remove 3sec delay
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

        #TODO: use python FFMPEG or ask for download
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
        if cfg.ext_videos == 'Y':
            print("Compressing video file with FFMPEG (ASF to WEBM)")
            source_dir = self.dir_extr
            source_file = "video.asf"
            dest_dir = self.dir_conv
            dest_file = "video.webm"

            #TODO: use python FFMPEG or ask for download
            try:
                cmd = cfg.ffmpeg_file 
                cmd += " -y -loglevel -8 -stats -hwaccel auto -i "
                cmd += "\"" + source_dir + "\\" + source_file + "\""
                for i, instrument in enumerate(data_order):
                    audio_in = dest_dir + "\\" + instrument + ".ogg"
                    if os.path.exists(audio_in):
                        cmd += " -i \"" + audio_in + "\""
                #cmd += " -ss " + str(self.delay) + "ms -filter_complex amix=inputs="     # Intro Skip #TODO: remove 3sec delay
                cmd += " -filter_complex amix=inputs="                 # Intro Skip #TODO: remove 3sec delay
                cmd += str(int(i)) 
                cmd += ":duration=longest -c:v libvpx -quality good -crf 12 -b:v 2000K -map 0:v:0? -an -sn -map_chapters -1 -f webm "
                cmd += "\"" +  dest_dir + "\\" + dest_file + "\""
                #print("Command: " + cmd)    # DEBUG
                subprocess.run(cmd)
            except:
                print("FFMPEG.exe not found")
        else:
            print("Video convertion skiped")

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
        #print("Disk dir:\t", songs_dir)    # DEBUG

    def append(self, song:Song,  debug = False):
        self.Songs.append(song)

    def log_start(self, cfg:Settings, debug = False):
        cfg.log_file = cfg.dir_work
        cfg.log_file += "\\"
        cfg.log_file += "songs.csv"

        log_file = open(cfg.log_file, "w", newline="")
        log_line = ""
        log_line += "Artista,"
        log_line += "Canción,"
        log_line += "Disco,"
        log_line += "Año,"
        log_line += "Song ID,"
        log_line += "Band ID,"
        log_line += "Disc ID,"
        log_line += "Dif:G,"
        log_line += "Dif:R,"
        log_line += "Dif:D,"
        log_line += "Dif:V,"
        log_line += "Dif:B,"
        log_line += "\n"

        log_file.write(log_line)
        log_file.close()

class Track(object):
    def __init__(self, cbr_chart:cbr.Cbr.Charts, debug = False):
        self.id_num = cbr_chart.inst_id.value
        self.name = cbr_chart.inst_id.name
        self.info = int.from_bytes(cbr_chart.chart_info)   #Unknown usage
        pulse = []
        for this_pulse in cbr_chart.pulse:
            pulse_dict = {
                "time": this_pulse.time,
                "type": this_pulse.type
            }
            pulse.append(pulse_dict)
        self.pulse = sorted(pulse, key=lambda item: item['time'])
        
        if self.id_num < 3:
            self.Diffs = []
            for diff_raw in cbr_chart.inst.diff_charts:
                diff_clean = Chart(diff_raw, self.id_num, debug)
                self.Diffs.append(diff_clean)

        if self.name == "vocals":
            self.Lyrics = Lyrics(cbr_chart.vocals, debug)

    def extract(self, song:Song, debug = False):
        file = song.dir_extr
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
                this_dir = song.dir_extr
                this_dir += "\\"
                this_dir += self.name
                this_diff.extract(this_dir, debug)
        
        if self.name == "vocals":
            this_dir = song.dir_extr
            this_dir += "\\"
            this_dir += self.name
            self.Lyrics.extract(song, debug)

class Chart(object):
    def __init__(self, cbr_diff:cbr.Cbr.Instrument, inst_id_num:int, debug = False):
        self.id_num = cbr_diff.diff.value
        self.name = cbr_diff.diff.name
        self.info = cbr_diff.diff_info  #Unknown usage

        self.max_note = cbr_diff.num_frets_pts
        if debug:
            if self.max_note != 5:  #DEBUG
                print("<WARN>: Frets number is", self.max_note)
        notes = []

        for i, this_color in enumerate(cbr_diff.frets_on_fire):
            for this_note in this_color.frets_wave:
                if inst_id_num < 2:
                    fixed_note = 4 - i
                else:   #TODO Double check if drums ok
                    fixed_note = i

                note_dict = {
                    "time": this_note.time,
                    "len": this_note.len,
                    "note": fixed_note,
                    "mods": this_note.mods
                }
                notes.append(note_dict)
        self.notes = sorted(notes, key=lambda item: item['time'])
 
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
        pitch = []
        harms = []
        verses = []
        self.info = int.from_bytes(cbr_vocal.vocal_info)  #Unknown usage

        for verse_raw in cbr_vocal.lyrics:
            verse_clean = Verse(verse_raw, debug)
            verses.append(verse_clean)
        
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

            pitch.append(pitch_dict)
            harms.append(harm_dict)

        self.verses = sorted(verses, key=lambda item: item.time)
        self.pitch = sorted(harms, key=lambda item: item['time'])
        self.harm = sorted(harms, key=lambda item: item['time'])

    def extract(self, song:Song, debug = False):
        file = song.dir_extr
        file += "\\"
        file += "vocals"
        file += "_"
        file += "pitch"
        file += "-"
        file += str(self.info)
        file += ".csv"
        dicts_to_csv(file, self.pitch)
        
        file = song.dir_extr
        file += "\\"
        file += "vocals"
        file += "_"
        file += "harm"
        file += "-"
        file += str(self.info)
        file += ".csv"
        dicts_to_csv(file, self.harm)

        file = song.dir_extr
        file += "\\"
        file += "vocals"
        file += "_"
        file += "lyrics"    
        file += "-"
        file += str(self.info)
        file += ".lrc"  
        
        lrc_file = open(file, "w", encoding='utf-8')

        lrc_file.write("[ar:" + song.band + "]\n")
        lrc_file.write("[al:" + song.disc + "]\n")
        lrc_file.write("[ti:" + song.name + "]\n")
        #offset = +3000
        offset = +0000
        lrc_file.write("[offset:" + str(offset) + "]\n") #TODO: remove offset

        for this_verse in self.verses:
            lrc_line = "[" 
            lrc_line += ticks_to_clock(this_verse.time, SAMPLE_RATE)
            lrc_line += "]"
            lrc_file.write(lrc_line)
            for this_syll in this_verse.syllables:
                lrc_line = "<"
                lrc_line += ticks_to_clock(this_syll['time'], SAMPLE_RATE)
                lrc_line += ">"
                text = this_syll['note']
                if text.endswith('- '):
                    text = text[:-2]
                elif text.endswith('-'):
                    text = text[:-1]
                else:
                    text = text + ' '
                while text.find("  ") > 0:
                    text = text.replace("  ", " ")
                lrc_line += text
                lrc_file.write(lrc_line)
            lrc_line = "\n"
            lrc_file.write(lrc_line)

        lrc_file.close()

class Verse(object):
    def __init__(self, cbr_verse:cbr.Cbr.Verse, debug = False):
        self.time = cbr_verse.time_start
        self.mods = cbr_verse.mods
        self.len = cbr_verse.time_end - cbr_verse.time_start
        
        dur_sum = 0
        syllables = []
        for this_syll in cbr_verse.text_block:
            syll_dict = {
                "time": this_syll.time_start,
                "len": (this_syll.time_end - this_syll.time_start),
                "note": this_syll.text,
                "mods": this_syll.type
            }
            dur_sum += syll_dict['len']
            syllables.append(syll_dict)
        self.syllables = sorted(syllables, key=lambda item: item['time'])

        if debug:
            if dur_sum != cbr_verse.len:
                print("<WARN>: Dur and Len are diferent")
