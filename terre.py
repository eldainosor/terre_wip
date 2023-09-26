#!/usr/bin/python
# Python script
# Made by Envido32

import os
import time
import csv
from terre_ex import *
from collections import Counter

# Config Constants 
debug = True       #DEBUG
sec_tick = 44092    #TODO: find if it can be fixed or calibrated
const_res = 480     #Like RB
#const_res = 192    #Like GH
#TODO: Res=480000 a recalc ticks with variable BPM from [event]

'''
def fixtiming(time):
    this_bpm = 1000*60*sec_tick/this_res
    res = 2*diff_count.most_common(1)[0][0]
    return time
'''

if __name__ == "__main__":

    print(" >>> EXTRACTOR TODO EL ROCK (RECARGADO) <<< ")

    cfg = Settings(debug)
    pl = Playlist(cfg, debug)
  
    # Raw extraction
    for k, filename in enumerate(pl.files):
        k += 1
        n = len(pl.files)
        print("Analizing (", int(k) , "/" , int(n) , ")")   # DEBUG

        this_song = Song(cfg, filename, debug)
        pl.append(this_song)

        this_song.create_metadata(debug)
        this_song.extract_icon(cfg, debug)
        this_song.extract_preview(cfg, debug)
        this_song.extract_audio(cfg, debug)
        this_song.extract_album(cfg, debug)
        this_song.extract_background(cfg, debug)
        this_song.extract_video(cfg, debug)
        this_song.extract_charts(cfg, debug)

        # Save Kaitai Log
        # COMMON HEADER

        # Extract Pulses (file_cbr)        
        os.chdir(this_song.dir_extr)  
        head_lens = []
        chart_info = []
        for this_inst in this_song.cbr.charts:
            this_inst_name = this_inst.inst_id.name
            chart_info.append(this_inst.chart_info)
            file_name = "pulse_" + this_inst_name + ".csv"
            pulse_file = open(file_name, "w", newline="")
            csv_writer = csv.writer(pulse_file)
            data_in = [ "time", 
                    "type" , 
                    "DELTA" , 
                    "MIN",
                    "SEC",
                    "cht_nfo", 
                    "trk_nfo",
                      ]
            csv_writer.writerow(data_in)
            
            inst_pulse = this_inst.pulse

            this_chart_info = this_inst.chart_info
            this_trk_info = this_song.cbr.meta_end
                
            head_lens.append(len(inst_pulse))
            #print(this_inst_name + " header len: " + str(int(len(inst_pulse))))       # DEBUG
            #print(this_inst_name + " header len: " + str(this_inst.num_pulse))    # DEBUG
            
            # chart = Chart(chart_path)

            csv_rows = []
            first_tick = 0
            last_tick = 0
            aux = 0
            for this_pulse in inst_pulse:
                
                sec = ( this_pulse.time ) / ( sec_tick )
                #sec *= 60
                #sec /= bpm
                min = int(sec / 60)
                sec %= 60

                if first_tick == 0:
                    first_tick = this_pulse.time

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
            delta_pulse = []
            for this_pulse in inst_pulse:
                delta_pulse.append(this_pulse.time - aux)
                aux = this_pulse.time

            delta_count = Counter(delta_pulse)      #TODO:Remove Counter?
            #aux = delta_count.most_common(1)[0]
            #res = 2*aux[0]
            res = 2*delta_count.most_common(1)[0][0]

            csv_writer.writerows(csv_rows)
            pulse_file.close()

        '''
        chart_info.append(this_song.cbr.vocals.head.chart_info)
        try:
            chart_info.append(this_song.cbr.band.chart_info)
        except:
            chart_info.append(int(0))
        '''
        
        largest_number = head_lens[0]
        for number in head_lens:
            if number > largest_number:
                largest_number = number
        
        # print(" > BIGGER header len:" + str(largest_number))  # DEBUG

        diff_info = []
        for this_inst in this_song.cbr.charts:
            this_inst_name = this_inst.inst_id.name
            if this_inst.inst_id.value < 3:
                for this_diff in this_inst.inst.diff_charts:
                    this_diff_name = this_diff.diff.name
                    diff_info.append(this_diff.diff_info)
                    file_name = "charts_" + this_inst_name + "_" + this_diff_name + ".csv"
                    chart_file = open(file_name, "w", newline="")
                    csv_writer = csv.writer(chart_file)
                    
                    this_chart_info = this_inst.chart_info
                    this_trk_info = this_song.cbr.meta_end
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
                    for i, this_color in enumerate(this_diff.frets_on_fire):
                        for this_note in this_color.frets_wave:
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
        '''
        diff_info.append(this_song.cbr.vocals.vocal_info)

        file_name = "charts_vocals.csv"
        chart_file = open(file_name, "w", newline="")
        csv_writer = csv.writer(chart_file)
        
        #   0       1       2   3       4    5       6       7
        # [Scale, StartA, EndA, Mod, NoteA, StartB, NoteB, EndB]
        data_in = [ "TIME", 
                    "LEN", 
                    "mod", 
                    "scale", 
                    "noteA",
                    "noteB",
                    "NULL",
                    "startA",
                    "startB",
                    "NULL",
                    "endA",
                    "endB",
                    "NULL",
                    ]
        csv_writer.writerow(data_in)

        csv_rows = []
        csv_rows_sorted = []
                
        for this_wave in this_song.cbr.vocals.wave_form:
            # Pitch: [Scale, StartA, EndA, Mod, NoteA, StartB, NoteB, EndB]
            this_note = this_wave.note
            #this_note %= 5
            data_in = [ this_wave.start,     # Time
                        this_wave.end - this_wave.start,   #Len
                        this_wave.mod,     # Mod
                        this_wave.scale,     # Scale
                        this_wave.note,     # NoteA
                        this_wave.note_harm,     # NoteB
                        this_wave.note_harm - this_wave.note,    # NULL
                        this_wave.start,     # StartA
                        this_wave.start_harm,     # StartB
                        this_wave.start_harm - this_wave.start,    # NULL
                        this_wave.end,     # EndA
                        this_wave.end_harm,     # EndB
                        this_wave.end_harm - this_wave.end    # NULL
                        ]
            csv_rows.append(data_in)

        csv_rows_sorted = sorted(csv_rows, key=lambda item: item[0])

        csv_writer.writerows(csv_rows_sorted)
        chart_file.close()
        '''

        # Create chart file
        ts_num = 4  #TODO: Find real ts (time signature - compas)
        ts_dem = 2  # this is 2^ts_dem
        #res = 82680/pow(2,ts_dem)   #TODO: Find real resolution (ticks per 1/4 note)
        bpm = 1000*60*sec_tick/res   #TODO: Find real bpm (beats per minute)
        new_file = open("notes.chart", "w", encoding='utf-8')

        new_file.write("[Song]")
        new_file.write("\n{")
        new_file.write("\n  Name = \"" + this_song.name + "\"")
        new_file.write("\n  Artist = \"" + this_song.band + "\"")
        new_file.write("\n  Charter = \"Next Level\"")
        new_file.write("\n  Album = \"" + this_song.disc + "\"")
        new_file.write("\n  Year = \", " + str(this_song.year) + "\"")
        new_file.write("\n  Offset = 3")    #TODO: revome 3sec delay
        #new_file.write("\n  Offset = 0")    #TODO: revome 3sec delay
        new_file.write("\n  Resolution = " + str(int(res)))
        new_file.write("\n  Player2 = bass")
        new_file.write("\n  Difficulty = " + str(this_song.diffs[4]))
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
        beats = 0
        prev_pulse_time = 0
        prev_pulse_type = 0
        prev_bpm = 0
        prev_ts_n = 0
        start_pulse_time = 0
        offset_pulse = 0
        #TODO fix sync
        for this_pulse in this_song.cbr.charts[0].pulse:
            #if offset_pulse > 0:
            if start_pulse_time > 0:

                # Start pulse
                if this_pulse.type != 2:
                    beats += 1
                else:
                    # Save and Reestart
                    if beats > 1:
                        this_ts_n = int (beats / 2)
                        this_res = this_pulse.time - start_pulse_time
                        this_res /= this_ts_n
                        this_bpm = 1000*60*sec_tick/this_res
                        if this_ts_n != prev_ts_n:
                            new_file.write("\n  " + str(start_pulse_time + offset_pulse) + " = TS " + str(this_ts_n))
                            prev_ts_n = this_ts_n
                        if this_bpm != prev_bpm:
                            new_file.write("\n  " + str(start_pulse_time + offset_pulse) + " = B " + str(int(this_bpm)))
                            prev_bpm = this_bpm                        
                    start_pulse_time = this_pulse.time
                    beats = 1
            
            else:
                if this_pulse.type == 3 and prev_pulse_type == 2:
                    offset_pulse = prev_pulse_time
                    start_pulse_time = prev_pulse_time
                    beats = 2
                
            prev_pulse_time = this_pulse.time
            prev_pulse_type = this_pulse.type
        new_file.write("\n}\n")

        new_file.write("[Events]")
        new_file.write("\n{")

        '''
        # Lyrics extraction
        for this_phrase in this_song.cbr.vocals.lyrics:
            new_file.write("\n  " + str(this_phrase.info[0]) + " = E \"phrase_start\"")
            for this_syll in this_phrase.text_block:
                new_file.write("\n  " + str(this_syll.time_start) + " = E \"lyric " + str(this_syll.text) + "\"")
            new_file.write("\n  " + str(this_phrase.info[1]) + " = E \"phrase_end\"")
                
        new_file.write("\n}\n")

        new_file.write("[HardKeyboard]")    #DEBUG Vocals test
        #new_file.write("[Vocals]")    #DEBUG Vocals test
        new_file.write("\n{")

        wave_list = []
        harm_list = []
        sp_list = []
        for this_wave in this_song.cbr.vocals.wave_form:
            # Pitch: [Scale, StartA, EndA, Mod, NoteA, StartB, NoteB, EndB]
            this_note = this_wave.note + 12 * this_wave.scale
            this_note_harm = this_wave.note_harm + 12 * this_wave.scale
            #this_note %= 5
            wave_list.append([this_wave.start, "N", this_note, this_wave.end - this_wave.start]) 
            harm_list.append([this_wave.start_harm, "E", this_note_harm, this_wave.end_harm - this_wave.start_harm]) 
            if this_wave.mod:
                wave_list.append([this_wave.start, "S", this_note, this_wave.end - this_wave.start]) 
                #wave_list.append([this_wave.start, "S", 2, this_wave.end - this_wave.start]) 
            
        harm_list.extend(wave_list)
        harm_list.extend(sp_list)
        sorted_harms = []
        sorted_harms = sorted(harm_list, key=lambda item: item[0])
        
        for this_sorted_notes in sorted_harms:
            new_file.write("\n  " + str(this_sorted_notes[0]) + " = " + str(this_sorted_notes[1])  + " " + str(this_sorted_notes[2]) + " " + str(this_sorted_notes[3]))

        new_file.write("\n}\n")
        '''
        
        for this_inst in this_song.cbr.charts:
            if this_inst.inst_id.value < 3:
                this_inst_name = this_inst.inst_id.name
                
                match this_inst_name:
                    case "guitar":
                        this_inst_name = "Single"
                    case "rhythm":
                        this_inst_name = "DoubleBass"
                    case "drums":
                        this_inst_name = "Drums"
                    case _:
                        this_inst_name = ""
            
                for this_diff in this_inst.inst.diff_charts:
                    this_diff_name = this_diff.diff.name
                
                    new_file.write("[" + this_diff_name.capitalize() + this_inst_name + "]")
                    new_file.write("\n{")

                    notes_list = []
                    sp_list = []
                    hopo_list = []
                    strum_list = []
                    mods_list = []
                    for i, this_color in enumerate(this_diff.frets_on_fire):
                        for this_note in this_color.frets_wave:
                            if this_inst_name == "Drums":
                                note_color = i
                            else:
                                note_color = 4 - i
                            
                            #TODO: note modes is:   0x00 NOTE "N", 0x01 "S LEN" STAR, 0x10 HOPO "N 5", 0x20 UP,  0x30 DOWN, 0x02 ???
                            notes_list.append([this_note.time, "N", note_color, this_note.len])

                            has_sp = this_note.mods & 0x01
                            has_hopo = this_note.mods & 0x10
                            has_strum = this_note.mods & 0x20
                            has_other = this_note.mods & 0x0E  #DEBUG

                            if has_sp:
                                sp_list.append([this_note.time, "S", note_color, this_note.len])
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
        inst_pulse = this_song.cbr.charts[2].pulse
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
                
        # Save to log
        os.chdir(cfg.dir_work)
        csv_name = "songs.csv"
        new_file = open(csv_name, "a", newline="")
        csv_writer = csv.writer(new_file)
        data_in = [ this_song.band,
                    this_song.name,
                    this_song.disc,
                    this_song.year,
                    this_song.song_id,
                    this_song.band_id,
                    this_song.disc_id,
                    this_song.diffs[0], # Guitar
                    this_song.diffs[1], # Rhythm
                    this_song.diffs[2], # Drums
                    this_song.diffs[3], # Vocal
                    this_song.diffs[4], # Band
                    this_song.track_info,
                    chart_info[0],    # Guitar
                    chart_info[1],    # Rhythm
                    chart_info[2],    # Drums
                    chart_info[3],    # Vocal
                    #chart_info[4],    # Band
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
                    first_tick,
                    last_tick,
                    #this_chart_info,
        ]

        csv_writer.writerow(data_in)
        new_file.close()

        # Show time and ETA
        total_tm = this_song.print_elapsed_time()
        eta_time = time.gmtime((total_tm / k ) * (n - k))
        print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))
        
    # Convert to Clone Hero (needs FFMPEG)
    if cfg.convert == 'Y':
        # Loop for each song
        for k, this_song in enumerate(pl.Songs):
            k += 1
            n = len(pl.Songs)
            print(" >> Converting (", int(k) , "/" , int(n) , "): ", this_song.name) 

            start_song = time.time()
            local = time.strftime("%H:%M:%S", time.localtime(start_song))
            print("Song start: ", local)

            this_song.convert_metadata(debug)
            this_song.convert_icon(debug)
            this_song.convert_preview(cfg, debug)
            this_song.convert_audio(cfg, debug)
            this_song.convert_album(debug)
            this_song.convert_background(debug)
            this_song.convert_video(cfg, debug)
            this_song.convert_charts(cfg, debug)

            # Show time and ETA
            elapsed_tm = time.time() - start_song
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_tm))
            print("This song took:\t" , elapsed)
            total_tm = cfg.print_elapsed_time()
            eta_time = time.gmtime((total_tm / k ) * (n - k))
            print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))

    cfg.print_elapsed_time()
    