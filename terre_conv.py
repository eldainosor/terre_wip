#!/usr/bin/python
# Python script
# Made by Envido32

from collections import Counter

sam_rate = 44100    # HiRes digital sampling rate
#sam_rate = 44056    # HiRes NTSC
const_res = 480     # Like RB
#const_res = 192    # Like GH
SECONDS_PER_MINUTE = 60.0
MILIS_PER_SECS = 1000.0

def DisToTime(tickStart:int, tickEnd:int, bpm:int, resolution:int):
    deltaTick = tickEnd - tickStart
    time = ( SECONDS_PER_MINUTE * deltaTick ) / ( bpm * resolution )
    return time

def TimeToDis(timeStart:int, timeEnd:int, bpm:int, resolution:int):
    deltaTime = timeEnd - timeStart
    dis = ( deltaTime * bpm * resolution ) / SECONDS_PER_MINUTE
    return dis

def DisToBpm(tickStart:int, tickEnd:int, timeStart:int, timeEnd:int, resolution:int):
    deltaTick = tickEnd - tickStart
    deltaTime = timeEnd - timeStart
    bpm = ( SECONDS_PER_MINUTE * deltaTick ) / ( deltaTime * resolution)
    return bpm

def TimeToBpm(timeStart:int, timeEnd:int, beats:int, resolution:int):
    deltaTime = timeEnd - timeStart
    bpm = ( MILIS_PER_SECS * SECONDS_PER_MINUTE * sam_rate * beats ) / ( 2 * deltaTime )
    return bpm

'''
def TimeToBpm(tickStart:int, tickEnd:int, timeStart:int, timeEnd:int, resolution:int):
    deltaTick = tickEnd - tickStart
    deltaTime = timeEnd - timeStart
    bpm = ( resolution * deltaTime ) / ( SECONDS_PER_MINUTE * deltaTick )
    return bpm
'''

def TickScaling(tick:int, originalResolution:int, outputResolution:int):
    tick = tick * outputResolution / originalResolution
    return tick

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
        if offset_pulse > 0:       #TODO sync offset wrong?
            if this_pulse['type'] != 2:
                beats += 1
            else:
                if beats > 1:
                    this_bpm = TimeToBpm(start_pulse_time, this_pulse['time'], beats, const_res)

                    if this_ts_n != prev_ts_n:
                        if prev_ts_n == 0:
                            this_sync = {
                                "time":     int(0),
                                "type":     "TS",
                                "value":    int(this_ts_n)
                            }
                            sync_track_data.append(this_sync)
                        this_sync = {
                            "time":     int(start_pulse_time + offset_pulse),
                            "type":     "TS",
                            "value":    int(this_ts_n)
                        }
                        sync_track_data.append(this_sync)
                        prev_ts_n = this_ts_n
                    if this_bpm != prev_bpm:
                        if prev_bpm == 0:
                            this_sync = {
                                "time":     int(0),
                                "type":     "B",
                                "value":    int(this_bpm)
                            }
                            sync_track_data.append(this_sync)
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
                start_pulse_time = prev_pulse_time
                beats = 2
                print("Offset:", offset_pulse / sam_rate)
        prev_pulse_time = this_pulse['time']
        prev_pulse_type = this_pulse['type']
        
    sync_track_data = sorted(sync_track_data, key=lambda item: item['time'])
    delay = offset_pulse / sam_rate
    return ( sync_track_data, res , delay)

def analize_charts(charts:dict, bmp_data:dict, debug = False):
    notes_list = []
    sp_list = []
    hopo_list = []
    strum_list = []
    mods_list = []
    for this_note in charts:
        #TODO: if len == 2000: then len = 0
        #TODO: note modes is:   0x00 NOTE "N", 0x01 "S LEN" STAR, 0x10 HOPO "N 5", 0x20 UP,  0x30 DOWN, 0x02 ???
        note_in = {
            "time":     int(this_note['time']),
            "type":     "N " + str(this_note['note']),
            "value":    int(this_note['len'])
        }
        notes_list.append(note_in)
        
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
        if has_hopo:
            note_in = {
                "time":     int(this_note['time']),
                "type":     "N 5",
                "value":    int(this_note['len'])
            }
            hopo_list.append(note_in)
        if has_strum:
            # TODO: What kind of modifier is this?
            note_in = {
                "time":     int(this_note['time']),
                "type":     "N 9",
                "value":    int(this_note['len'])
            }
            strum_list.append(note_in)
        if has_other:
            # TODO: What other kind of modifier are there?
            note_in = {
                "time":     int(this_note['time']),
                "type":     "N 10",
                "value":    int(this_note['len'])
            }
            print("<WARN>: Other fret mod found: " + str(has_other))   #DEBUG
            mods_list.append(note_in)
    sp_list.extend(notes_list)
    sp_list = sorted(sp_list, key=lambda item: item['time'])

    first_timing = 0
    last_timing = 0
    last_len = 0
    
    prev_timing = 0
    prev_type = "N"
    prev_len = 0

    sp_counting = 0
    sp_list_clean = []
    #TODO: Star Power works OK on CH and Moonscraper... not YARG, why?
    for this_star in sp_list:
        this_time = this_star['time']
        this_type = this_star['type']
        this_value = this_star['value']

        match sp_counting:
            case 0:     #Waiting for S
                if this_type.startswith("N"):
                    sp_counting = 0 #Waiting for S
                elif this_type.startswith("S"):
                    first_timing = this_time
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
                sp_list_clean.append(note_in)
                sp_counting = 0
            case _:
                sp_counting = 0
        prev_timing = this_time
        prev_len = this_value
        prev_type = this_type
        
    notes_list.extend(sp_list_clean)
    #notes_list.extend(hopo_list)
    #notes_list.extend(strum_list)
    notes_list = sorted(notes_list, key=lambda item: item['type'])
    notes_list = sorted(notes_list, key=lambda item: item['time'])

    return notes_list