#!/usr/bin/python
# Python script
# Made by Envido32

from collections import Counter

sec_tick = 44092    #TODO: find if it can be fixed or calibrated
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
    bpm = 1000*60*sec_tick/res   #TODO: Find real bpm (beats per minute)

    sync_track_data = []
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
                    this_res = this_pulse['time'] - start_pulse_time
                    this_res /= this_ts_n
                    this_bpm = 1000*60*sec_tick/this_res
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
                start_pulse_time = prev_pulse_time
                beats = 2
        prev_pulse_time = this_pulse['time']
        prev_pulse_type = this_pulse['type']
    return ( sync_track_data, res )
