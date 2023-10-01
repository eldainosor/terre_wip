#!/usr/bin/python
# Python script
# Made by Envido32

from collections import Counter

sam_rate = 44100    # HiRes digital sampling rate
#sam_rate = 44056    # NTSC
#sam_rate = 44092    #TODO: find if it can be fixed or calibrated
const_res = 480     #Like RB
#const_res = 192    #Like GH

def analize_pulse(inst_pulse, debug = False):
    aux = 0
    delta_pulse = []
    for this_pulse in inst_pulse:
        delta_pulse.append(this_pulse['time'] - aux)
        aux = this_pulse['time']

    delta_count = Counter(delta_pulse)      #TODO:Remove Counter?
    #aux = delta_count.most_common(1)[0]
    #res = 2*aux[0]
    res = 2*delta_count.most_common(1)[0][0]

    # Create chart file
    ts_num = 4  #TODO: Find real ts (time signature - compas)
    ts_dem = 2  # this is 2^ts_dem
    #res = 82680/pow(2,ts_dem)   #TODO: Find real resolution (ticks per 1/4 note)
    bpm = 1000*60*sam_rate/res   #TODO: Find real bpm (beats per minute)

    sync_track_data = []
    this_tpb = res  # Tick per beat
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
    for this_pulse in inst_pulse:
        #if offset_pulse > 0:       #TODO sync offset wrong?
        if start_pulse_time > 0:
            # Start pulse
            if this_pulse['type'] != 2:
                beats += 1
            else:
                # Save and Reestart
                if beats > 1:
                    this_ts_n = int (beats / 2)
                    this_tpb = this_pulse['time'] - start_pulse_time
                    this_tpb /= this_ts_n
                    this_bpm = 1000*60*sam_rate/this_tpb
                    if this_ts_n != prev_ts_n:
                        this_sync = {
                            "time":     int(start_pulse_time + offset_pulse),
                            "type":     "TS",
                            "value":    int(this_ts_n)
                        }
                        sync_track_data.append(this_sync)
                        prev_ts_n = this_ts_n
                    if this_bpm != prev_bpm:
                        this_sync = {
                            "time":     int(start_pulse_time + offset_pulse),
                            "type":     "B",
                            "value":    int(this_bpm)
                        }
                        sync_track_data.append(this_sync)
                        prev_bpm = this_bpm                        
                start_pulse_time = this_pulse['time']
                beats = 1
        else:
            if this_pulse['type'] == 3 and prev_pulse_type == 2:
                offset_pulse = prev_pulse_time
                offset_pulse = 0
                start_pulse_time = prev_pulse_time
                beats = 2
        prev_pulse_time = this_pulse['time']
        prev_pulse_type = this_pulse['type']
    return ( sync_track_data, res )

def analize_charts(charts:dict, bmp_data:dict, debug = False):
    clean_charts = []

    notes_list = []
    sp_list = []
    hopo_list = []
    strum_list = []
    mods_list = []
    for this_note in charts:
        #TODO: verify Drums order
        '''
        if this_inst_name == "Drums":
            this_note['note'] = i
        else:
            this_note['note'] = 4 - i
        '''
        #TODO: if len == 2000: then len = 0
        #TODO: note modes is:   0x00 NOTE "N", 0x01 "S LEN" STAR, 0x10 HOPO "N 5", 0x20 UP,  0x30 DOWN, 0x02 ???
        note_in = {
            "time":     int(this_note['time']),
            "type":     "N " + str(this_note['note']),
            "value":    int(this_note['len'])
        }
        notes_list.append(note_in)
        #notes_list.append([this_note['time'], "N", this_note['note'], this_note['len']])

        has_sp = this_note['mods'] & 0x01
        has_hopo = this_note['mods'] & 0x10
        has_strum = this_note['mods'] & 0x20
        has_other = this_note['mods'] & 0x0E  #DEBUG

        if has_sp:
            note_in = {
                "time":     int(this_note['time']),
                "type":     "S " + str(this_note['note']),
                "value":    int(this_note['len'])
            }
            sp_list.append(note_in)
            #sp_list.append([this_note['time'], "S", this_note['note'], this_note['len']])
            #sp_list.append([this_note['time'], "S", 2, this_note['len']])
        
        if has_hopo:
            note_in = {
                "time":     int(this_note['time']),
                "type":     "N 5",
                "value":    int(this_note['len'])
            }
            hopo_list.append(note_in)
            #hopo_list.append([this_note['time'], "N", 5, this_note['len']])

        if has_strum:
            # TODO: What kind of modifier is this?
            note_in = {
                "time":     int(this_note['time']),
                "type":     "N 9",
                "value":    int(this_note['len'])
            }
            strum_list.append(note_in)
            #strum_list.append([this_note['time'], "N", 9, this_note['len']])
            #strum_list.append([this_note['time'], "N", 5, this_note['len']])

        if has_other:
            # TODO: What other kind of modifier are there?
            note_in = {
                "time":     int(this_note['time']),
                "type":     "N 10",
                "value":    int(this_note['len'])
            }
            print("Other fret mod FOUND: " + str(has_other))   #DEBUG
            mods_list.append(note_in)
            #mods_list.append([this_note['time'], "N", 10, this_note['len']])
            #mods_list.append([this_note['time'], "N", 5, this_note['len']])

    sp_list_old = []
    sp_list_old.extend(sp_list)
    sp_list.extend(notes_list)
    sorted_stars = []
    sorted_stars = sorted(sp_list, key=lambda item: item['time'])

    first_timing = 0
    #first_len = 0
    last_timing = 0
    last_len = 0
    
    prev_timing = 0
    prev_type = "N"
    prev_len = 0

    sp_counting = 0

    sp_list_new = []
    
    #TODO: Star Power works OK on CH and Moonscraper... not YARG, why?
    for this_star in sorted_stars:
        this_time = this_star['time']
        this_type = this_star['type']
        this_value = this_star['value']

        match sp_counting:
            case 0:     #Waiting for S
                if this_type.startswith("N"):
                    sp_counting = 0 #Waiting for S
                elif this_type.startswith("S"):
                    first_timing = this_time
                    #first_len = this_len
                    last_timing = this_time
                    last_len = this_value
                    sp_counting = 1 #Expect N
            case 1:     #Expect N
                if prev_timing == this_time and prev_len == this_value:
                    sp_counting = 1 #Keep counting
                else:
                    if this_type.startswith("S") and prev_type.startswith("N"):
                        sp_counting = 1
                    else:
                        last_timing = prev_timing
                        last_len = prev_len
                        sp_counting = 2
            case 2:
                sp_len = last_timing 
                sp_len -= first_timing 
                sp_len += last_len
                note_in = {
                    "time":     int(first_timing),
                    "type":     "S 2",
                    "value":    int(sp_len)
                }
                sp_list_new.append(note_in)

                #sp_list_new.append([first_timing, "S", 2, sp_len])
                sp_counting = 0
            case _:
                sp_counting = 0
        prev_timing = this_time
        prev_len = this_value
        prev_type = this_type
        
    notes_list.extend(sp_list_new)
    #notes_list.extend(hopo_list)
    #notes_list.extend(strum_list)
    sorted_notes = []
    sorted_notes = sorted(notes_list, key=lambda item: item['time'])
    
    for this_sorted_note in sorted_notes:
        clean_charts.append(this_sorted_note)
        #new_file.write("\n  " + str(this_sorted_note[0]) + " = " + str(this_sorted_note[1]) + " " + str(this_sorted_note[2]) + " " + str(this_sorted_note[3]) )

    return clean_charts
    #new_file.write("\n}\n")