#!/usr/bin/python
# Python script
# Made by Envido32

from collections import Counter

SAMPLE_RATE = 44100    # HiRes digital sampling rate
#SAMPLE_RATE = 44056    # HiRes NTSC
RESOLUTION = 480     # Like RB
#RESOLUTION = 192    # Like GH
SECONDS_PER_MINUTE = 60.0
MILIS_PER_SECS = 1000.0

def DisToTime(tickStart:int, tickEnd:int, bpm:int):
    deltaTick = ( tickEnd - tickStart ) / RESOLUTION
    time = ( MILIS_PER_SECS * SECONDS_PER_MINUTE * deltaTick ) / ( bpm )
    return time

def TimeToDis(timeStart:int, timeEnd:int, bpm:int):
    deltaTime = ( timeEnd - timeStart ) / SAMPLE_RATE
    dis = ( deltaTime * bpm * RESOLUTION ) / ( MILIS_PER_SECS *  SECONDS_PER_MINUTE )
    return dis

def SwapTimeForDis(time:int, bpms:dict):
    bpm = FindBpm(bpms, time)
    tick = TimeToDis(bpm['time'], time, bpm['value'])
    tick += bpm['tick']
    return tick

def DisToBpm(tickStart:int, tickEnd:int, timeStart:int, timeEnd:int):
    deltaTick = ( tickEnd - tickStart ) / RESOLUTION
    deltaTime = ( timeEnd - timeStart ) / SAMPLE_RATE
    bpm = ( MILIS_PER_SECS * SECONDS_PER_MINUTE * deltaTick ) / ( deltaTime )
    return bpm

def TimeToBpm(timeStart:int, timeEnd:int, beats:int):
    deltaTime = ( timeEnd - timeStart ) / SAMPLE_RATE
    bpm = ( MILIS_PER_SECS * SECONDS_PER_MINUTE * beats ) / ( deltaTime )
    return bpm

def FirstBpm(timeEnd:int):
    bpm = TimeToBpm(0, timeEnd, 2)
    return bpm

def FindBpm(bpms:dict, time:int):
    bpm_out = bpms[1]
    for this_bpm in bpms:
        if this_bpm['type'] == "B":
            if this_bpm['time'] < time:
                bpm_out = this_bpm
    return bpm_out

def TickScaling(tick:int, originalResolution:int, outputResolution:int):
    tick = tick * outputResolution / originalResolution
    return tick

def analize_pulse(inst_pulse, debug = False):
    res = RESOLUTION

    # Create chart file
    ts_num = 4  #TODO: Find real ts (time signature - compas)
    #ts_dem = 2  # this is 2^ts_dem
    #res = 82680/pow(2,ts_dem)   #TODO: Find real resolution (ticks per 1/4 note)
    #bpm = 1000*60*SAMPLE_RATE/res   #TODO: Find real bpm (beats per minute)

    sync_track_data = []
    this_bpm = 120
    this_tick = 0
    this_ts_n = ts_num
    #this_ts_d = ts_dem
    beats = 0
    prev_pulse_time = 0
    prev_pulse_type = 0
    prev_bpm = 0
    prev_ts_n = 0
    prev_bpm_time = 0
    prev_bpm_tick = 0
    start_pulse_time = 0
    offset_pulse = 0
    for this_pulse in inst_pulse:
        if offset_pulse > 0:
            if this_pulse['type'] != 2:
                beats += 1
            else:
                if beats > 1:
                    this_ts_n = beats / 2
                    this_bpm = TimeToBpm(start_pulse_time, this_pulse['time'], this_ts_n)
                    if prev_bpm_time == 0:
                        this_tick = TimeToDis(0, this_pulse['time'], this_bpm)
                    else:
                        this_tick = TimeToDis(prev_bpm_time, this_pulse['time'], prev_bpm)
                    this_tick += prev_bpm_tick

                    if this_ts_n != prev_ts_n:
                        if prev_ts_n == 0:
                            this_sync = {
                                "time":     int(0),
                                "tick":     int(0),
                                "type":     "TS",
                                "value":    int(this_ts_n)
                            }
                            sync_track_data.append(this_sync)
                        this_sync = {
                            "time":     int(this_pulse['time']),
                            "tick":     int(this_tick),
                            "type":     "TS",
                            "value":    int(this_ts_n)
                        }
                        sync_track_data.append(this_sync)
                        prev_ts_n = this_ts_n
                    if this_bpm != prev_bpm:
                        if prev_bpm == 0:
                            first_bpm = FirstBpm(start_pulse_time)
                            this_sync = {
                                "time":     int(0),
                                "tick":     int(0),
                                "type":     "B",
                                "value":    int(this_bpm)
                            }
                            sync_track_data.append(this_sync)
                        this_sync = {
                            "time":     int(this_pulse['time']),
                            "tick":     int(this_tick),
                            "type":     "B",
                            "value":    int(this_bpm)
                        }
                        sync_track_data.append(this_sync)
                        prev_bpm = this_bpm
                        prev_bpm_time = this_pulse['time']
                        prev_bpm_tick = this_tick
                start_pulse_time = this_pulse['time']
                beats = 1
        else:
            if this_pulse['type'] == 3 and prev_pulse_type == 2:
                offset_pulse = prev_pulse_time
                start_pulse_time = prev_pulse_time
                beats = 2
                print("Offset:", offset_pulse / SAMPLE_RATE)
        prev_pulse_time = this_pulse['time']
        prev_pulse_type = this_pulse['type']
        
    #sync_track_data = sorted(sync_track_data, key=lambda item: item['time'])
    sync_track_data = sorted(sync_track_data, key=lambda item: item['tick'])
    delay = offset_pulse / SAMPLE_RATE
    return ( sync_track_data, res, delay )

def analize_charts(charts:dict, bpm_data:dict, debug = False):
    notes_list = []
    sp_list = []
    hopo_list = []
    strum_list = []
    mods_list = []
    for this_note in charts:
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

    for i, this_note in enumerate(notes_list):
        this_tick = SwapTimeForDis(this_note['time'], bpm_data)

        notes_list[i].update({'tick': int(this_tick)})
        if this_note['value'] > 2000:
            base_bpm = FindBpm(bpm_data, this_note['time'])
            len = TimeToDis(0, this_note['value'], base_bpm['value'])
        else:
            len = 0
        notes_list[i].update({'len': int(len)})

    #notes_list.extend(hopo_list)
    #notes_list.extend(strum_list)
    notes_list = sorted(notes_list, key=lambda item: item['type'])
    #notes_list = sorted(notes_list, key=lambda item: item['time'])
    notes_list = sorted(notes_list, key=lambda item: item['tick'])

    return notes_list
