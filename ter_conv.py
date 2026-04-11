#!/usr/bin/python
# Python script
# Made by Envido32

SAMPLE_RATE = 44100    # HiRes digital sampling rate
#SAMPLE_RATE = 44056    # HiRes NTSC
RESOLUTION = 480     # Like RB
#RESOLUTION = 192    # Like GH
SECONDS_PER_MINUTE = 60.0
MILIS_PER_SECS = 1000.0

def TimeToDis(timeStart:int, timeEnd:int, bpm_scaled:int):
    """Calcula ticks usando el BPM escalado (ej: 120000)."""
    deltaTime = (timeEnd - timeStart) / SAMPLE_RATE
    # Como el BPM ya viene multiplicado por 1000, dividimos por 1000 en la base
    dis = (deltaTime * bpm_scaled * RESOLUTION) / (MILIS_PER_SECS * SECONDS_PER_MINUTE)
    return dis

def SwapTimeForDis(time:int, bpms:list):
    """Calcula el tick absoluto de una nota basándose en la lista de BPMs."""
    bpm_node = FindBpm(bpms, time)
    # Calculamos distancia desde el tiempo del último cambio de BPM
    tick = TimeToDis(bpm_node['time'], time, bpm_node['value'])
    tick += bpm_node['tick']
    return tick

def TimeToBpm(timeStart:int, timeEnd:int, beats:int):
    """Calcula el BPM escalado por 1000 para el formato .chart."""
    deltaTime = (timeEnd - timeStart) / SAMPLE_RATE
    if deltaTime <= 0: return 120000
    bpm = (MILIS_PER_SECS * SECONDS_PER_MINUTE * beats) / (deltaTime)
    return int(bpm)

def FindBpm(bpms:list, time:int):
    """Busca el evento de BPM activo para un tiempo dado."""
    bpm_out = bpms[0]
    for this_bpm in bpms:
        if this_bpm['type'] == "B":
            if this_bpm['time'] <= time:
                bpm_out = this_bpm
    return bpm_out

def analyze_structure(pulses):
    """Algoritmo del visor HTML para encontrar el Inicio Real."""
    if len(pulses) < 4: return 0, 0
    offset_real = pulses[0]['time']
    index_real = 0
    for i in range(len(pulses) - 2):
        d1 = pulses[i+1]['time'] - pulses[i]['time']
        d2 = pulses[i+2]['time'] - pulses[i+1]['time']
        if d1 > 100 and d2 > 100 and abs(d1 - d2) < 100:
            offset_real = pulses[i]['time']
            index_real = i
            break
    return offset_real, index_real

def analize_pulse(inst_pulse, debug=False, use_fake_bpm=True):
    res = RESOLUTION
    offset_real, start_idx = analyze_structure(inst_pulse)
    sync_track_data = []
    
    time_shift = 0 if use_fake_bpm else offset_real
    
    # 1. Inicialización
    if use_fake_bpm:
        intro_bpm = TimeToBpm(0, offset_real, start_idx)
        sync_track_data.append({"time": 0, "tick": 0, "type": "B", "value": intro_bpm})
        sync_track_data.append({"time": 0, "tick": 0, "type": "TS", "value": 4})
        current_tick = start_idx * res
    else:
        sync_track_data.append({"time": 0, "tick": 0, "type": "B", "value": 120000})
        sync_track_data.append({"time": 0, "tick": 0, "type": "TS", "value": 4})
        current_tick = 0

    pulses_to_process = inst_pulse[start_idx:]
    prev_bpm_value = sync_track_data[0]['value']
    prev_bpm_time = offset_real
    prev_bpm_tick = current_tick
    start_pulse_time = offset_real
    beats = 2

    for i, this_pulse in enumerate(pulses_to_process):
        relative_time = int(this_pulse['time'] - time_shift)
        
        if this_pulse['type'] != 2:
            beats += 1
        else:
            if beats > 1:
                this_ts_n = int(beats / 2)
                this_bpm_scaled = TimeToBpm(start_pulse_time, this_pulse['time'], this_ts_n)
                
                # CAMBIO: Calculamos el tick exacto basándonos en el tiempo real
                # para que coincida perfectamente con SwapTimeForDis
                current_tick = TimeToDis(prev_bpm_time, this_pulse['time'], prev_bpm_value) + prev_bpm_tick

                if this_ts_n != (sync_track_data[-1]['value'] if sync_track_data else 4):
                    sync_track_data.append({"time": relative_time, "tick": int(current_tick), "type": "TS", "value": this_ts_n})
                
                if abs(this_bpm_scaled - prev_bpm_value) > 100:
                    sync_track_data.append({"time": relative_time, "tick": int(current_tick), "type": "B", "value": this_bpm_scaled})
                    # Actualizamos anclas de tiempo y tick
                    prev_bpm_value = this_bpm_scaled
                    prev_bpm_time = this_pulse['time']
                    prev_bpm_tick = current_tick
                    
            start_pulse_time = this_pulse['time']
            beats = 1

    return (sorted(sync_track_data, key=lambda x: x['tick']), res, 0.0 if use_fake_bpm else (offset_real / SAMPLE_RATE))

def analize_charts(charts:dict, bpm_data:list, debug=False, time_shift=0):
    """
    charts: Notas originales del CBR (tiempos absolutos).
    bpm_data: Tu SyncTrack generado.
    time_shift: El 'offset_real' (tiempo de la basura en samples).
    """
    notes_list = []
    sp_list = []
    hopo_list = []
    strum_list = []
    mods_list = []
    for this_note in charts:
        # IMPORTANTE: Restamos la basura al tiempo de la nota antes de calcular el tick
        # para que coincida con el nuevo 'tiempo cero' del SyncTrack.
        relative_note_time = this_note['time'] - time_shift
        
        # Si la nota estaba dentro de la basura, la ignoramos (opcional)
        if relative_note_time < 0:
            continue

        this_tick = SwapTimeForDis(relative_note_time, bpm_data)
        
        # El cálculo del sustain (len) también debe ser relativo
        if this_note['len'] > 2000:
            base_bpm = FindBpm(bpm_data, relative_note_time)
            note_len = TimeToDis(0, this_note['len'], base_bpm['value'])
        else:
            note_len = 0

        #TODO: note modes is:   0x00 NOTE "N", 0x01 "S LEN" STAR, 0x10 HOPO "N 5", 0x20 UP,  0x30 DOWN, 0x02 ???
        #                                                         0x11 HOPO+STAR "N 5", 0x21 UP+STAR,  0x31 DOWN+STAR
        note_in = {
            "tick":     int(this_tick),
            "type":     "N " + str(this_note['note']),
            "len":    int(note_len),
            "mods": this_note['mods']
        }
        notes_list.append(note_in)
        
        has_sp = this_note['mods'] & 0x01
        has_hopo = this_note['mods'] & 0x10
        has_strum = this_note['mods'] & 0x20
        has_other = this_note['mods'] & 0x0E  #DEBUG

        if has_sp:
            note_in = {
                "tick":     int(this_tick),
                "type":     "S " + str(this_note['note']),
                "len":    int(note_len),
                "mods": this_note['mods']
            }
            sp_list.append(note_in)
        if has_hopo:
            note_in = {
                "tick":     int(this_tick),
                #"type":     "N 5",
                "type":     "W " + str(this_note['note']),
                "len":    int(note_len),
                "mods": this_note['mods']
            }
            hopo_list.append(note_in)
        if has_strum:
            # TODO: What kind of modifier is this?
            note_in = {
                "tick":     int(this_tick),
                #"type":     "N 9",
                "type":     "K " + str(this_note['note']),
                "len":    int(note_len),
                "mods": this_note['mods']
            }
            strum_list.append(note_in)
        if has_other:
            # TODO: What other kind of modifier are there?
            note_in = {
                "tick":     int(this_tick),
                "type":     "N 10",
                "len":    int(note_len),
                "mods": this_note['mods']
            }
            print("<WARN>: Other fret mod found: " + str(has_other))   #DEBUG
            mods_list.append(note_in)
    sp_list.extend(notes_list)
    sp_list = sorted(sp_list, key=lambda item: item['tick'])
    hopo_list.extend(notes_list)
    hopo_list = sorted(hopo_list, key=lambda item: item['tick'])
    strum_list.extend(notes_list)
    strum_list = sorted(strum_list, key=lambda item: item['tick'])

    first_timing = 0
    last_timing = 0
    last_len = 0
    
    prev_timing = 0
    prev_type = "N"
    prev_len = 0

    sp_counting = 0
    sp_list_clean = []

    hopo_counting = 0
    hopo_list_clean = []
    prev_hopo_timing = 0
    prev_hopo_type = "N"
    prev_hopo_len = 0
    first_hopo_timing = 0
    last_hopo_timing = 0
    last_hopo_len = 0

    strum_counting = 0
    strum_list_clean = []
    prev_strum_timing = 0
    prev_strum_type = "N"
    prev_strum_len = 0
    first_strum_timing = 0
    last_strum_timing = 0
    last_strum_len = 0

    #TODO: Star Power works OK on CH and Moonscraper... not YARG, why?
    for this_star in sp_list:
        this_time = this_star['tick']
        this_type = this_star['type']
        this_value = this_star['len']

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
                    "tick":     int(first_timing),
                    "type":     "S 2",
                    "len":    int(sp_len),
                    "mods":     this_star['mods']
                }
                sp_list_clean.append(note_in)
                sp_counting = 0
            case _:
                sp_counting = 0
        prev_timing = this_time
        prev_len = this_value
        prev_type = this_type
        
    notes_list.extend(sp_list_clean)

    #TODO: Implement a way less hacky of considering these events.
    for this_hopo in hopo_list:
        this_hopo_time = this_hopo['tick']
        this_hopo_type = this_hopo['type']
        this_hopo_value = this_hopo['len']

        match hopo_counting:
            case 0:     #Waiting for H
                if this_hopo_type.startswith("N"):
                    hopo_counting = 0 #Waiting for W
                elif this_hopo_type.startswith("W"):
                    first_hopo_timing = this_hopo_time
                    last_hopo_timing = this_hopo_time
                    last_hopo_len = this_hopo_value
                    hopo_counting = 1 #Expect N
            case 1:     #Expect N
                if prev_hopo_timing == this_hopo_time and prev_hopo_len == this_hopo_value:
                    hopo_counting = 1 #Keep counting
                else:
                    if this_hopo_type.startswith("W") and prev_hopo_type.startswith("N"):
                        hopo_counting = 1
                    else:
                        last_hopo_timing = prev_hopo_timing
                        last_hopo_len = prev_hopo_len
                        hopo_counting = 2
            case 2:
                hopo_len = last_hopo_timing 
                hopo_len -= first_hopo_timing 
                hopo_len += last_hopo_len
                note_hopo_in = {
                    "tick":     int(first_hopo_timing),
                    "type":     "W 2",
                    "len":    int(hopo_len),
                    "mods":     this_hopo['mods']
                }
                hopo_list_clean.append(note_hopo_in)
                hopo_counting = 0
            case _:
                hopo_counting = 0

        prev_hopo_timing = this_hopo_time
        prev_hopo_len = this_hopo_value
        prev_hopo_type = this_hopo_type
        
    notes_list.extend(hopo_list_clean)

    for this_strum in strum_list:
        this_strum_time = this_strum['tick']
        this_strum_type = this_strum['type']
        this_strum_value = this_strum['len']

        match strum_counting:
            case 0:     #Waiting for S
                if this_strum_type.startswith("N"):
                    strum_counting = 0 #Waiting for K
                elif this_strum_type.startswith("K"):
                    first_strum_timing = this_strum_time
                    last_strum_timing = this_strum_time
                    last_strum_len = this_strum_value
                    strum_counting = 1 #Expect N
            case 1:     #Expect N
                if prev_strum_timing == this_strum_time and prev_strum_len == this_strum_value:
                    strum_counting = 1 #Keep counting
                else:
                    if this_strum_type.startswith("K") and prev_strum_type.startswith("N"):
                        strum_counting = 1
                    else:
                        last_strum_timing = prev_strum_timing
                        last_strum_len = prev_strum_len
                        strum_counting = 2
            case 2:
                strum_len = last_strum_timing 
                strum_len -= first_strum_timing 
                strum_len += last_strum_len
                note_strum_in = {
                    "tick":     int(first_strum_timing),
                    "type":     "K 2",
                    "len":    int(strum_len),
                    "mods":     this_strum['mods']
                }
                strum_list_clean.append(note_strum_in)
                strum_counting = 0
            case _:
                strum_counting = 0

        prev_strum_timing = this_strum_time
        prev_strum_len = this_strum_value
        prev_strum_type = this_strum_type
        
    notes_list.extend(strum_list_clean)

    #notes_list.extend(hopo_list)
    #notes_list.extend(strum_list)
    notes_list = sorted(notes_list, key=lambda item: item['type'])
    #notes_list = sorted(notes_list, key=lambda item: item['time'])
    notes_list = sorted(notes_list, key=lambda item: item['tick'])

    return sorted(notes_list, key=lambda item: (item['tick'], item['type']))