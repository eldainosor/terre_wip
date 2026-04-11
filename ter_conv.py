#!/usr/bin/python
# Python script
# Made by Envido32

SAMPLE_RATE = 44100    # HiRes digital sampling rate
RESOLUTION = 480       # Ticks por negra
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
    prev_bpm_tick = current_tick # Importante: Guardar el tick de referencia
    prev_ts_n = 4
    
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
                
                # CAMBIO CLAVE: Calculamos el tick del SyncTrack usando la misma fórmula que las notas
                # Esto elimina el drift acumulado.
                current_tick = TimeToDis(prev_bpm_time, this_pulse['time'], prev_bpm_value) + prev_bpm_tick

                if this_ts_n != prev_ts_n:
                    sync_track_data.append({
                        "time": relative_time,
                        "tick": int(current_tick),
                        "type": "TS",
                        "value": this_ts_n
                    })
                    prev_ts_n = this_ts_n
                
                if abs(this_bpm_scaled - prev_bpm_value) > 100:
                    sync_track_data.append({
                        "time": relative_time,
                        "tick": int(current_tick),
                        "type": "B",
                        "value": this_bpm_scaled
                    })
                    # Actualizamos referencias para el siguiente tramo de interpolación
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

        notes_list.append({
            "tick": int(this_tick),
            "type": "N " + str(this_note['note']),
            "len": int(note_len),
            "mods": this_note['mods']
        })
    
    return sorted(notes_list, key=lambda item: (item['tick'], item['type']))