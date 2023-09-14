#!/usr/bin/python
# Python script
# Made by Envido32
'''
Extra info about new variables name:
trk_vol > trk_info[7]
bpm	> chart_info
events	> pulse
event	> tick
speed	> diff_info
frets	> colour
spark	> note
timing	> time
type	> mods
speed	> vocal_info
water	> pitch
'''

import os, re, shutil
import subprocess
import time
import cbr, disc, band
import csv, configparser
from collections import Counter
# from chchart_parser.chart import Chart

# Config Constants 
data_order = ["head","guitar", "rhythm", "drums", "vocals", "song"]
inst_order = ["guitar", "rhythm", "drums", "vocals", "band"]
diff_order = ["easy", "medium", "hard"]
sec_tick = 44096
#TODO: Res=480000 a recalc ticks with variable BPM from [event]

if __name__ == "__main__":

    start_time = time.time()

    print(" >>> EXTRACTOR TODO EL ROCK (RECARGADO) <<< ")

    localtime = time.localtime(start_time)
    local = time.strftime("%H:%M:%S", localtime)
    print("Start time: ", local)

    #disc_dir = input("Elegi la unidad del disco ERDTV: ")[0].upper() + ":"
    #disc_dir = "E:" # DEBUG
    #mozart_dir = disc_dir + "\\install\\data\\mozart"
    mozart_dir = "D:\\Games\\Rythm\\ERDTV\\Mozart"  #TODO: Delete when done
    songs_dir = mozart_dir + "\\song"
    bands_dir = mozart_dir + "\\band"
    discs_dir = mozart_dir + "\\disc"
    work_dir = os.getcwd()
    output_dir = os.getcwd() + "\\erdtv"
    raw_dir = os.getcwd() + "\\raw"
    
    print("Working dir:\t [", work_dir, "]")

    # Analize files
    print(" > Analizing files... < " )
    print("Songs dir:\t[", songs_dir ,"]")
    os.chdir(songs_dir)

    dir_files = os.listdir(songs_dir)
    #print("Files in dir:\t",  dir_files)   # DEBUG

    cbr_files = []
    for filename in dir_files:
        if re.search("\.cbr$", filename):
            cbr_files.append(filename)

    n = len(cbr_files)

    # Create log file
    if n > 0:
        print("Songs found in dir:\t",  n)
        os.chdir(work_dir)
        csv_name = "songs.csv"
        new_file = open(csv_name, "w", newline="")
        csv_writer = csv.writer(new_file)
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
                    "S:G_0",
                    "S:G_1",
                    "S:G_2",
                    "S:R_0",
                    "S:R_1",
                    "S:R_2",
                    "S:D_0",
                    "S:D_1",
                    "S:D_2",
                    "S:V_0",
                    "Res",
                    "Last tick",
                    "BPM:cal",
        ]
        
        csv_writer.writerow(data_in)
        new_file.close()

    #print("Disk dir:\t", songs_dir)    # DEBUG

    # Output directories
    try:
        os.mkdir(raw_dir)
    except OSError as error:
        print("Output dir:\t[", raw_dir, "] already exists")
        
    # Raw extraction
    for k, filename in enumerate(cbr_files):
        k += 1
        start_song = time.time()
        local = time.strftime("%H:%M:%S", time.localtime(start_song))
        print("Song start: ", local)

        print("Analizing (", int(k) , "/" , int(n) , ")")   # DEBUG

        os.chdir(songs_dir)
        #working_file = open(filename, "rb")
        #file_id, ext = os.path.splitext(filename)
        #print("File ID = " + file_id)  # DEBUG test Kaitai

        # Read CBR file
        file_cbr = cbr.Cbr.from_file(filename)
        
        # Extract Song ID
        song_id = file_cbr.info.song_id     # Int vble
        song_id = str(hex(song_id)).upper().lstrip('0X')    # String formating
        print("Song ID = " + song_id)  # DEBUG test Kaitai

        # Extract Band ID
        band_id = file_cbr.info.band_id     # Int vble
        band_id = str(hex(band_id)).upper().lstrip('0X')    # String formating
        print("Band ID = " + band_id)  # DEBUG test Kaitai
        
        # Extract Disc ID
        disc_id = file_cbr.info.disc_id     # Int vble
        disc_id = str(hex(disc_id)).upper().lstrip('0X')    # String formating
        print("Disc ID = " + disc_id)  # DEBUG test Kaitai

        # Extract Year
        year = file_cbr.info.year
        print("Year = " + str(year))  # DEBUG test Kaitai
        
        # Extract Song Name
        song_name = str(file_cbr.info.song_name).rstrip('\x00')
        print("Song = " + file_cbr.info.song_name)  # DEBUG test Kaitai

        # Extract Difficulty
        difficulties = file_cbr.tracks.diff_level
        band_diff = int(0)
        for instrument in difficulties:
            band_diff += instrument
        difficulties[4] = int(band_diff / 4)
        
        track_info = file_cbr.tracks.trk_info[6]

        print("Diff. Guitar =\t" + str(difficulties[0]))  # DEBUG test Kaitai
        print("Diff. Rythm =\t" + str(difficulties[1]))  # DEBUG test Kaitai
        print("Diff. Drums =\t" + str(difficulties[2]))  # DEBUG test Kaitai
        print("Diff. Vocal =\t" + str(difficulties[3]))  # DEBUG test Kaitai
        print("Diff. Band =\t" + str(difficulties[4]))  # DEBUG test Kaitai
    
        # Analize Bands
        os.chdir(bands_dir)

        #dir_files = os.listdir(curr_dir) # DEBUG
        #print("Files in dir:", dir_files) # DEBUG

        # Read Band file
        file_band = band.Band.from_file(band_id + ".band")
        band_name = str(file_band.band_name).rstrip('\x00')
        print("Band = " + band_name)
        
        # Analize discs
        os.chdir(discs_dir)
        file_disc = disc.Disc.from_file(disc_id + ".disc")
        disc_name = str(file_disc.disc_name).rstrip('\x00')
        print("Disc = " + disc_name)
        disc_img = file_disc.image.png

        # Analize Background
        os.chdir(songs_dir)
        working_file = open(song_id + ".bgf", "rb")
        background_data = working_file.read(0x020C)
        background_img = working_file.read()
        working_file.close()

        # Analize Stems
        #print(" > Searching band... < " )
        working_file = open(song_id + ".au", "rb")
        song_data = working_file.read()
        flac_head = "fLaC".encode('U8')
        audio_data = song_data.split(flac_head)
        working_file.close()

        # Output Files
        new_song_dir = raw_dir + "\\" + band_name + " - " + song_name

        try:
            os.mkdir(new_song_dir)
        except OSError as error:
            print("[", new_song_dir , "] already exists")
        os.chdir(new_song_dir)

        new_file = open("background.png", "wb")
        new_file.write(background_img)
        new_file.close()
        
        new_file = open("album.png", "wb")
        new_file.write(disc_img)
        new_file.close()

        # Save steams
        for i, audio in enumerate(audio_data):
            data_order[i]
            new_file = open(data_order[i] + ".flac", "wb")
            new_file.write(flac_head)
            new_file.write(audio)
            new_file.close()

        # Copy preview
        source = songs_dir + "\\" + song_id
        dest = new_song_dir
        try:
            print("Copying preview...")
            shutil.copyfile(source + ".prv", dest  + "\\preview.wav")
        except:
            print("File [ ", dest,  "\\preview.wav ] already exists")

        # Copy video (slow)
        try:
            print("Copying video... ")
            #shutil.copyfile(source + ".vid", dest  + "\\video.asf")    #TODO do not comment
        except:
            print("File [ ", dest,  "\\video.asf ] already exists")

        # Copy icon
        #TODO extract from Disk (.ico to .png)
        source = work_dir
        dest = new_song_dir
        try:
            #print("Copying icon...")
            shutil.copyfile(source + "\\erdtv.png", dest  + "\\erdtv.png")
        except:
            print("File [ ", dest,  "\\erdtv.png ] already exists")

        # Save Kaitai Log
        # COMMON HEADER

        #ExtractEvents(file_cbr)        
        head_lens = []
        chart_info = []
        for this_inst in file_cbr.tracks.charts:
            this_inst_name = this_inst.head.instrument_id.name
            chart_info.append(this_inst.head.chart_info)
            file_name = "pulse_" + this_inst_name + ".csv"
            pulse_file = open(file_name, "w", newline="")
            csv_writer = csv.writer(pulse_file)
            data_in = [ "time", 
                    "type" , 
                    "DIFF" , 
                    "MIN",
                    "SEC",
                    "cht_nfo", 
                    "trk_nfo",
                      ]
            csv_writer.writerow(data_in)
            
            inst_pulse = this_inst.head.pulse

            this_chart_info = this_inst.head.chart_info
            this_trk_info = file_cbr.tracks.trk_info[6]
                
            head_lens.append(len(inst_pulse))
            #print(this_inst_name + " header len: " + str(int(len(inst_pulse))))       # DEBUG
            #print(this_inst_name + " header len: " + str(this_inst.head.num_pulse))    # DEBUG
            
            # chart = Chart(chart_path)

            csv_rows = []
            last_tick = 0
            aux = 0
            for this_pulse in inst_pulse:
                
                sec = ( this_pulse.time ) / ( sec_tick )
                #sec *= 60
                #sec /= bpm
                min = int(sec / 60)
                sec %= 60

                last_tick = this_pulse.time
                data_in = [ this_pulse.time, 
                            this_pulse.type, 
                            this_pulse.time - aux,
                            min,
                            sec,
                            this_chart_info, 
                            this_trk_info,
                              ]
                aux = this_pulse.time
                csv_rows.append(data_in)
            
            res = 0
            aux = 0
            i = 0
            diff_pulse = []
            for this_pulse in inst_pulse:
                diff_pulse.append(this_pulse.time - aux)
                aux = this_pulse.time

            diff_count = Counter(diff_pulse)
            #aux = diff_count.most_common(1)[0]
            #res = 2*aux[0]
            res = 2*diff_count.most_common(1)[0][0]

            csv_writer.writerows(csv_rows)
            pulse_file.close()

        chart_info.append(file_cbr.tracks.vocals.head.chart_info)
        try:
            chart_info.append(file_cbr.tracks.band.chart_info)
        except:
            chart_info.append(int(0))
        
        largest_number = head_lens[0]
        for number in head_lens:
            if number > largest_number:
                largest_number = number
        
        # print(" > BIGGER header len:" + str(largest_number))  # DEBUG

        '''
        diff_info = []
        for this_inst in file_cbr.tracks.charts:
            this_inst_name = this_inst.head.instrument_id.name
            for this_diff in this_inst.diff_charts:
                this_diff_name = this_diff.diff.name
                diff_info.append(this_diff.diff_info)
                file_name = "charts_" + this_inst_name + "_" + this_diff_name + ".csv"
                chart_file = open(file_name, "w", newline="")
                csv_writer = csv.writer(chart_file)
                
                this_chart_info = this_inst.head.chart_info
                this_trk_info = file_cbr.tracks.trk_info[6]
                this_diff_info = this_diff.diff_info
                
                data_in = [ "time", 
                        "len", 
                        "type", 
                        "fret", 
                        "MIN", 
                        "SEC",
                        "cht_nfo",
                        "trk_nfo",
                        "diff_nfo"
                        ]
                csv_writer.writerow(data_in)
                
                csv_rows = []
                csv_rows_sorted = []
                for i, this_colour in enumerate(this_diff.frets_on_fire):
                    for this_note in this_colour.frets_wave:
                        #TODO: Find real Rsolution, BPM and TS.
                        sec = ( this_note.time ) / ( sec_tick )
                        #sec *= 60
                        #sec /= bpm
                        min = int(sec / 60)
                        sec %= 60
                        data_in = [ this_note.time, 
                                this_note.len, 
                                this_note.mods, 
                                i, 
                                min, 
                                sec,
                                this_chart_info,
                                this_trk_info,
                                this_diff_info,
                                ]
                        csv_rows.append(data_in)
                
                csv_rows_sorted = sorted(csv_rows, key=lambda item: item[0])

                csv_writer.writerows(csv_rows_sorted)
                chart_file.close()
        diff_info.append(file_cbr.tracks.vocals.vocal_info)
        '''

        # Create chart file
        ts_num = 4  #TODO: Find real ts (time signature - compas)
        ts_dem = 2  # this is 2^ts_dem
        #res = 82680/pow(2,ts_dem)   #TODO: Find real resolution (ticks per 1/4 note)
        bpm = 1000*60*sec_tick/res   #TODO: Find real bpm (beats per minute)
        new_file = open("notes.chart", "w", encoding='utf-8')

        new_file.write("[Song]")
        new_file.write("\n{")
        new_file.write("\n  Name = \"" + song_name + "\"")
        new_file.write("\n  Artist = \"" + band_name + "\"")
        new_file.write("\n  Charter = \"Next Level\"")
        new_file.write("\n  Album = \"" + disc_name + "\"")
        new_file.write("\n  Year = \", " + str(year) + "\"")
        new_file.write("\n  Offset = 3")    #TODO: revome 3sec delay
        #new_file.write("\n  Offset = 0")    #TODO: revome 3sec delay
        new_file.write("\n  Resolution = " + str(int(res)))
        new_file.write("\n  Player2 = bass")
        new_file.write("\n  Difficulty = " + str(difficulties[4]))
        new_file.write("\n  Genre = \"Rock Argentino\"")
        new_file.write("\n  MusicStream = \"song.ogg\"")
        new_file.write("\n  GuitarStream = \"guitar.ogg\"")
        new_file.write("\n  RhythmStream = \"rhythm.ogg\"")
        new_file.write("\n  DrumStream = \"drums.ogg\"")
        new_file.write("\n  VocalStream = \"vocals.ogg\"")
        new_file.write("\n}\n")

        new_file.write("[SyncTrack]")
        #TODO: Res=480000 a recalc ticks with variable BPM from [event]
        new_file.write("\n{")
        #new_file.write("\n  0 = TS " + str(ts_num) + " " + str(ts_dem))
        #new_file.write("\n  0 = TS " + str(ts_num))
        #new_file.write("\n  0 = B " + str(int(bpm)))

        # BMPs secuence
        #TODO analize pulse ts_num and bpm
        bpm_list_phrases = []
        prev_tick = 0
        start_tick = 0
        this_res = res
        this_bpm = bpm
        this_ts_n = ts_num
        #this_ts_d = ts_dem
        ts_count = 0
        prev_pulse_time = 0
        prev_pulse_type = 0
        prev_bpm = 0
        prev_ts_n = 0
        #TODO fix sync
        for this_pulse in file_cbr.tracks.charts[0].head.pulse:
            if this_pulse.time >= prev_pulse_time:
                # Start pulse
                if this_pulse.type == 2:
                    # Save and Reestart
                    if ts_count > 0 and prev_pulse_type == 1:                        
                        this_ts_n = int (ts_count / 2)
                        this_res = this_pulse.time - start_pulse.time
                        this_res /= this_ts_n
                        this_bpm = 1000*60*sec_tick/this_res
                        if this_ts_n != prev_ts_n:
                            new_file.write("\n  " + str(this_pulse.time) + " = TS " + str(this_ts_n))
                            prev_ts_n = this_ts_n
                        if this_bpm != prev_bpm:
                            new_file.write("\n  " + str(this_pulse.time) + " = B " + str(int(this_bpm)))
                            prev_bpm = this_bpm
                    # First Pulse
                    start_pulse = this_pulse
                    ts_count = 1

                elif this_pulse.type == 3 and prev_pulse_type == 2:
                    ts_count += 1
                elif this_pulse.type == 0 and prev_pulse_type == 3:
                    ts_count += 1
                elif this_pulse.type == 1 and prev_pulse_type == 0:
                    ts_count += 1
                elif this_pulse.type == 0 and prev_pulse_type == 1:
                    ts_count += 1
                else:
                    ts_count = 0
            else:
                ts_count = 0
            
            prev_pulse_time = this_pulse.time
            prev_pulse_type = this_pulse.type
        new_file.write("\n}\n")

        new_file.write("[Events]")
        new_file.write("\n{")

        # Lyrics extraction
        for this_phrase in file_cbr.tracks.vocals.lyrics:
            new_file.write("\n  " + str(this_phrase.info[0]) + " = E \"phrase_start\"")
            for this_syll in this_phrase.text_block:
                new_file.write("\n  " + str(this_syll.time_start) + " = E \"lyric " + str(this_syll.text) + "\"")
            new_file.write("\n  " + str(this_phrase.info[1]) + " = E \"phrase_end\"")
                
        new_file.write("\n}\n")

        #TODO: Add waveform of lyrics in [HARM1]
        '''
        new_file.write("[HARM1]")
        new_file.write("\n{")

        harm_list = []
        lyrics_list = []
        wave_list = []
        types_list = []
        for this_phrase in file_cbr.tracks.vocals.lyrics:
            types_list.append([this_syll.time_start, "T" , 105, this_phrase.info[4]])
            lyrics_list.append([this_syll.time_start, "N" , 105, this_phrase.info[1] - this_phrase.info[0]])
            lyrics_list.append([this_syll.time_start, "N" , 105, this_phrase.info[5]])
            for this_syll in this_phrase.text_block:
                types_list.append([this_syll.time_start, "T" , 116, this_syll.type])
                lyrics_list.append([this_syll.time_start, "E" , this_syll.text, " "])            

        for this_wave in file_cbr.tracks.vocals.wave_form:
            wave_list.append([this_wave.pitch[1], this_wave.pitch[0] , this_wave.pitch[4], this_wave.pitch[2] - this_wave.pitch[1]]) 
        
        harm_list.extend(lyrics_list)
        harm_list.extend(wave_list)
        harm_list.extend(types_list)
        sorted_harms = []
        sorted_harms = sorted(harm_list, key=lambda item: item[0])
        
        for this_sorted_notes in sorted_harms:
                    new_file.write("\n  " + str(this_sorted_notes[0]) + " = " + str(this_sorted_notes[1]) + " " + str(this_sorted_notes[2]) + " " + str(this_sorted_notes[3]) )

        new_file.write("\n}\n")
        '''

        for this_inst in file_cbr.tracks.charts:
            this_inst_name = this_inst.head.instrument_id.name
            
            match this_inst_name:
                case "guitar":
                    this_inst_name = "Single"
                case "rhythm":
                    this_inst_name = "DoubleBass"
                case "drums":
                    this_inst_name = "Drums"
                case _:
                    this_inst_name = ""
            
            for this_diff in this_inst.diff_charts:
                this_diff_name = this_diff.diff.name
            
                new_file.write("[" + this_diff_name.capitalize() + this_inst_name + "]")
                new_file.write("\n{")

                notes_list = []
                sp_list = []
                hopo_list = []
                strum_list = []
                mods_list = []
                for i, this_colour in enumerate(this_diff.frets_on_fire):
                    for this_note in this_colour.frets_wave:
                        if this_inst_name == "Drums":
                            note_colour = i
                        else:
                            note_colour = 4 - i
                        
                        #TODO: note modes is:   0x00 NOTE "N", 0x01 "S LEN" STAR, 0x10 HOPO "N 5", 0x20 UP,  0x30 DOWN, 0x02 ???
                        notes_list.append([this_note.time, "N", note_colour, this_note.len])

                        has_sp = this_note.mods & 0x01
                        has_hopo = this_note.mods & 0x10
                        has_strum = this_note.mods & 0x20
                        has_other = this_note.mods & 0x0E  #DEBUG

                        if has_sp:
                            sp_list.append([this_note.time, "S", note_colour, this_note.len])
                            #sp_list.append([this_note.time, "S", 2, this_note.len])
                        
                        if has_hopo:
                            hopo_list.append([this_note.time, "N", 5, this_note.len])

                        if has_strum:
                            # TODO: What kind of modifier is this?
                            strum_list.append([this_note.time, "N", 9, this_note.len])
                            #strum_list.append([this_note.time, "N", 5, this_note.len])
    
                        if has_other:
                            # TODO: What other kind of modifier are there?
                            print("Other fret mod FOUND: " + str(has_other))   #DEBUG
                            #mods_list.append([this_note.time, "N", 10, this_note.len])
                            #mods_list.append([this_note.time, "N", 5, this_note.len])

                sp_list_old = []
                sp_list_old.extend(sp_list)
                sp_list.extend(notes_list)
                sorted_stars = []
                sorted_stars = sorted(sp_list, key=lambda item: item[0])

                first_timing = 0
                first_len = 0
                last_timing = 0
                last_len = 0
                
                prev_timing = 0
                prev_type = "N"
                prev_len = 0

                sp_counting = 0

                sp_list_new = []
                
                #TODO: Star Power works OK on CH and Moonscraper... not YARG, why?
                for this_timing, this_type, this_note, this_len in sorted_stars:
                    match sp_counting:
                        case 0:     #Waiting for S
                            if this_type == "N":
                                sp_counting = 0 #Waiting for S
                            elif this_type == "S":
                                first_timing = this_timing
                                first_len = this_len
                                last_timing = this_timing
                                last_len = this_len
                                sp_counting = 1 #Expect N
                        case 1:     #Expect N
                            if prev_timing == this_timing and prev_len == this_len:
                                sp_counting = 1 #Keep counting
                            else:
                                if this_type == "S" and prev_type == "N":
                                    sp_counting = 1
                                else:
                                    last_timing = prev_timing
                                    last_len = prev_len
                                    sp_counting = 2
                        case 2:
                            sp_len = last_timing 
                            sp_len -= first_timing 
                            sp_len += last_len
                            sp_list_new.append([first_timing, "S", 2, sp_len])
                            sp_counting = 0
                        case _:
                            sp_counting = 0
                    prev_timing = this_timing
                    prev_len = this_len
                    prev_type = this_type
                    
                notes_list.extend(sp_list_new)
                #notes_list.extend(hopo_list)
                #notes_list.extend(strum_list)
                sorted_notes = []
                sorted_notes = sorted(notes_list, key=lambda item: item[0])
                
                for this_sorted_note in sorted_notes:
                    new_file.write("\n  " + str(this_sorted_note[0]) + " = " + str(this_sorted_note[1]) + " " + str(this_sorted_note[2]) + " " + str(this_sorted_note[3]) )

                new_file.write("\n}\n")


        #DEBUG BPM testing with DrumsExp
        new_file.write("[ExpertDrums]")
        new_file.write("\n{")

        notes_list = []
        inst_pulse = file_cbr.tracks.charts[2].head.pulse
        for this_pulse in inst_pulse:
            #aux = 3 - block.type
            aux = this_pulse.type + 1
            #aux += 2
            #aux %= 4
            notes_list.append([this_pulse.time, "N", aux, "0"])

        sorted_notes = sorted(notes_list, key=lambda item: item[0])

        for this_sorted_note in sorted_notes:
            new_file.write("\n  " + str(this_sorted_note[0]) + " = " + str(this_sorted_note[1]) + " " + str(this_sorted_note[2]) + " " + str(this_sorted_note[3]) )

        new_file.write("\n}\n")
        
        new_file.close()
                
        # Save metadata
        config = configparser.ConfigParser()
        config.add_section("song")

        config.set("song", "artist", band_name)
        config.set("song", "name", song_name)
        config.set("song", "album", disc_name)
        config.set("song", "year", str(year))
        config.set("song", "diff_guitar", str(difficulties[0]))
        config.set("song", "diff_bass", str(difficulties[1]))
        config.set("song", "diff_drums", str(difficulties[2]))
        config.set("song", "diff_vocals", str(difficulties[3]))
        config.set("song", "diff_band", str(difficulties[4]))
        config.set("song", "icon", "erdtv")
        config.set("song", "genre", "Rock Argentino")
        config.set("song", "charter", "Next Level")
        config.set("song", "banner_link_a", "http://www.elrockdetuvida.com/website/index.php")
        config.set("song", "link_name_a", "Homepage")
        config.set("song", "loading_phrase", "Viví la experiencia de interpretar los temas de tus bandas favoritas del rock nacional.")
        config.set("song", ";video_start_time" , "3000")    #TODO: remove 3sec delay
        config.set("song", "delay", "3000")                 #TODO: remove 3sec delay

        config.set("song", "diff_rhythm", "-1")
        config.set("song", "diff_drums_real", "-1")
        config.set("song", "diff_keys", "-1")
        config.set("song", "diff_guitarghl", "-1")
        config.set("song", "diff_bassghl", "-1")
        config.set("song", "diff_rhythm_ghl", "-1")
        config.set("song", "diff_guitar_coop_ghl", "-1")
        config.set("song", "diff_guitar_coop", "-1")
        config.set("song", "preview_start_time", "-1")
        config.set("song", "pro_drums", "0")
        config.set("song", "five_lane_drums", "0")

        new_file = open("song.ini", "w", encoding='utf-8')
        config.write(new_file)
        new_file.close()

        # Save to log
        os.chdir(work_dir)
        csv_name = "songs.csv"
        new_file = open(csv_name, "a", newline="")
        csv_writer = csv.writer(new_file)
        data_in = [ band_name,
                    song_name,
                    disc_name,
                    year,
                    song_id,
                    band_id,
                    disc_id,
                    difficulties[0], # Guitar
                    difficulties[1], # Rhythm
                    difficulties[2], # Drums
                    difficulties[3], # Vocal
                    difficulties[4], # Band
                    track_info,
                    chart_info[0],    # Guitar
                    chart_info[1],    # Rhythm
                    chart_info[2],    # Drums
                    chart_info[3],    # Vocal
                    chart_info[4],    # Band
                    #diff_info[0],  # Guitar-Easy
                    #diff_info[1],  # Guitar-Norm
                    #diff_info[2],  # Guitar-Hard
                    #diff_info[3],  # Rhythm-Easy
                    #diff_info[4],  # Rhythm-Norm
                    #diff_info[5],  # Rhythm-Hard
                    #diff_info[6],  # Drums-Easy
                    #diff_info[7],  # Drums-Norm
                    #diff_info[8],  # Drums-Hard
                    #diff_info[9],  # Vocals
                    res,
                    last_tick,
                    this_chart_info,
        ]

        csv_writer.writerow(data_in)
        new_file.close()

        # Show time and ETA
        elapsed_tm = time.time() - start_song
        elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_tm))
        print("This song took:\t" , elapsed)
        total_tm = time.time() - start_time
        total = time.strftime("%H:%M:%S", time.gmtime(total_tm))
        print("Total time took:\t" , total)
        eta_time = time.gmtime((total_tm / k ) * (n - k))
        print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))
        
    # Convert to Clone Hero (needs FFMPEG)
    #convert = input("Convertir a Clone Hero? (esto puede tomar bastante tiempo) [y/n]: ")[0].upper()
    convert = 'Y'  # DEBUG
    #convert = 'N'  # DEBUG
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
        #n = len(songs_list)

        # Loof for each song
        for j, this_song in enumerate(songs_list):
            j += 1
            #i = songs_list.index(this_song) + 1
            print(" >> Converting (", int(j) , "/" , int(len(songs_list)) , "): ", this_song) 

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
            try:
                #print("Copying album...")
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
            try:
                #print("Copying icon...")
                copy_file = "\\erdtv.png"
                source_file = source_dir + copy_file
                dest_file = dest_dir + copy_file
                shutil.copyfile(source_file, dest_file)
            except:
                print("File [ ", dest_file, " ] already exists")

            # Copy charts file
            try:
                #print("Copying metadata...")
                copy_file = "\\notes.chart"
                source_file = source_dir + copy_file
                dest_file = dest_dir + copy_file
                shutil.copyfile(source_file, dest_file)
            except:
                print("File [ ", dest_file, " ] already exists")

            # Copy metadata file
            try:
                #print("Copying metadata...")
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
                #cmd = cmd + " -y -stats -i "    # DEBUG Verbose 
                cmd = cmd + "\"" + source_file + "\""
                cmd = cmd + " -c:a libvorbis -b:a 320k " 
                cmd = cmd + "\"" + dest_file + "\""
                #print("Command: " + cmd)    # DEBUG
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
                    cmd = cmd + " -af adelay=3000:all=1 -c:a libvorbis -b:a 320k "      #Skipp 3sec #TODO: remove 3sec delay
                    #cmd = cmd + " -c:a libvorbis -b:a 320k "                           #Skipp 3sec #TODO: remove 3sec delay
                    cmd = cmd + "\"" + dest_file + "\""
                    #print("Command: " + cmd)    #DEBUG
                    subprocess.run(cmd)
                except:
                    print("FFMPEG.exe not found")

            # Convert video (VERY slow)
            try:
                print("Compressing video file with FFMPEG (ASF to WEBM)")
                copy_file = "\\video"
                source_file = source_dir + copy_file + ".asf"
                dest_file = dest_dir + copy_file + ".webm"
                
                cmd = ffmpeg_file 
                cmd = cmd + " -y -loglevel -8 -stats -hwaccel auto -i "
                cmd = cmd + "\"" + source_file + "\""
                for i, instrument in enumerate(data_order):
                    audio_in = dest_dir + "\\" + instrument + ".ogg"
                    if os.path.exists(audio_in):
                        cmd = cmd + " -i \"" + audio_in + "\""
                #cmd = cmd + " -ss 3000ms -filter_complex amix=inputs="     # Intro Skip #TODO: remove 3sec delay
                cmd = cmd + " -filter_complex amix=inputs="                 # Intro Skip #TODO: remove 3sec delay
                cmd = cmd + str(int(i)) 
                cmd = cmd + ":duration=longest -c:v libvpx -quality good -crf 12 -b:v 2000K -map 0:v:0? -an -sn -map_chapters -1 -f webm "
                cmd = cmd + "\"" + dest_file + "\""
                print("Command: " + cmd)    # DEBUG
                subprocess.run(cmd)
            except:
                print("FFMPEG.exe not found")

            # Show time and ETA
            elapsed_tm = time.time() - start_song
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_tm))
            print("This song took:\t" , elapsed)
            total_tm = time.time() - start_time
            total = time.strftime("%H:%M:%S", time.gmtime(total_tm))
            print("Total time took:\t" , total)
            eta_time = time.gmtime((total_tm / j ) * (n - j))
            print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))

    total_tm = time.time() - start_time
    total = time.strftime("%H:%M:%S", time.gmtime(total_tm))
    print("All tasks took: " , total)
