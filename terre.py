#!/usr/bin/python
# Python script
# Made by Envido32

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
                    "BPM:G",
                    "BPM:R",
                    "BPM:D",
                    "BPM:V",
                    "BPM:B",
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
        
        song_vol = file_cbr.tracks.trk_vol

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
            #print("Copying preview...")
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
        bpms = []
        for this_inst in file_cbr.tracks.charts:
            this_inst_name = this_inst.head.instrument_id.name
            bpms.append(this_inst.head.bpm)
            file_name = "events_" + this_inst_name + ".csv"
            event_file = open(file_name, "w", newline="")
            csv_writer = csv.writer(event_file)
            data_in = [ "time", 
                    "type" , 
                    "DIFF" , 
                    "MIN",
                    "SEC",
                    "bpm", 
                    "vol" ]
            csv_writer.writerow(data_in)
            
            inst_events = this_inst.head.events

            bpm = this_inst.head.bpm
            vol = file_cbr.tracks.trk_vol
                
            head_lens.append(len(inst_events))
            #print(this_inst_name + " header len: " + str(int(len(inst_events))))       # DEBUG
            #print(this_inst_name + " header len: " + str(this_inst.head.num_events))    # DEBUG
            
            # chart = Chart(chart_path)

            csv_rows = []
            last_tick = 0
            aux = 0
            for block in inst_events:
                
                sec = ( block.time ) / ( sec_tick )
                #sec *= 60
                #sec /= bpm
                min = int(sec / 60)
                sec %= 60

                last_tick = block.time
                data_in = [ block.time, 
                            block.type, 
                            block.time - aux,
                            min,
                            sec,
                            bpm, 
                            vol ]
                aux = block.time
                csv_rows.append(data_in)
            
            res = 0
            aux = 0
            i = 0
            diff_events = []
            for block in inst_events:
                diff_events.append(block.time - aux)
                aux = block.time

            diff_count = Counter(diff_events)
            #aux = diff_count.most_common(1)[0]
            #res = 2*aux[0]
            res = 2*diff_count.most_common(1)[0][0]

            csv_writer.writerows(csv_rows)
            event_file.close()

        bpms.append(file_cbr.tracks.vocals.head.bpm)
        try:
            bpms.append(file_cbr.tracks.band.bpm)
        except:
            bpms.append(int(0))
        
        largest_number = head_lens[0]
        for number in head_lens:
            if number > largest_number:
                largest_number = number
        
        # print(" > BIGGER header len:" + str(largest_number))  # DEBUG

        #ExtractCharts(file_cbr)
        
        speeds = []
        
        for this_inst in file_cbr.tracks.charts:
            this_inst_name = this_inst.head.instrument_id.name
            for this_diff in this_inst.diff_charts:
                this_diff_name = this_diff.diff.name
                speeds.append(this_diff.speed)
                file_name = "charts_" + this_inst_name + "_" + this_diff_name + ".csv"
                chart_file = open(file_name, "w", newline="")
                csv_writer = csv.writer(chart_file)
                
                bpm = this_inst.head.bpm
                vol = file_cbr.tracks.trk_vol
                speed = this_diff.speed
                
                data_in = [ "time", 
                        "len", 
                        "type", 
                        "fret", 
                        "MIN", 
                        "SEC",
                        "bpm",
                        "vol",
                        "speed"
                        ]
                csv_writer.writerow(data_in)
                
                csv_rows = []
                csv_rows_sorted = []
                for i, this_fret in enumerate(this_diff.frets_on_fire):
                    for this_spark in this_fret.frets_wave:
                        #TODO: Find real Rsolution, BPM and TS.
                        sec = ( this_spark.timing ) / ( sec_tick )
                        #sec *= 60
                        #sec /= bpm
                        min = int(sec / 60)
                        sec %= 60
                        data_in = [ this_spark.timing, 
                                this_spark.len, 
                                this_spark.type, 
                                i, 
                                min, 
                                sec,
                                bpm,
                                vol,
                                speed
                                ]
                        csv_rows.append(data_in)
                
                csv_rows_sorted = sorted(csv_rows, key=lambda item: item[0])

                csv_writer.writerows(csv_rows_sorted)
                chart_file.close()
        speeds.append(file_cbr.tracks.vocals.speed)


        # Create chart file

        ts_num = 4  #TODO: Find real ts (time signature - compas)
        ts_dem = 2  # this is 2^ts_dem
        #res = 82680/pow(2,ts_dem)   #TODO: Find real resolution (ticks per 1/4 note)
        bpm = 1000*60*sec_tick/res   #TODO: Find real bpm (beats per minute)
        new_file = open("notes.chart", "w", encoding='utf-8')

        new_file.write("[Song]")
        new_file.write("\n{")
        new_file.write("\n\tName = \"" + song_name + "\"")
        new_file.write("\n\tArtist = \"" + band_name + "\"")
        new_file.write("\n\tAlbum = \"" + disc_name + "\"")
        new_file.write("\n\tYear = \", " + str(year) + "\"")
        new_file.write("\n\tCharter = \"Next Level\"")
        new_file.write("\n\tOffset = 3")
        new_file.write("\n\tPlayer2 = bass")
        new_file.write("\n\tDifficulty = " + str(difficulties[4]))
        new_file.write("\n\tGenre = \"Rock Argentino\"")
        new_file.write("\n\tGuitarStream = \"guitar.ogg\"")
        new_file.write("\n\tRhythmStream = \"rhythm.ogg\"")
        new_file.write("\n\tDrumStream = \"drums.ogg\"")
        new_file.write("\n\tVocalStream = \"vocals.ogg\"")
        new_file.write("\n\tMusicStream = \"song.ogg\"")
        new_file.write("\n\tResolution = " + str(int(res)))
        new_file.write("\n}\n")

        new_file.write("[SyncTrack]")
        new_file.write("\n{")
        new_file.write("\n\t0 = B " + str(int(bpm)))
        new_file.write("\n\t0 = TS " + str(ts_num) + " " + str(ts_dem))
        new_file.write("\n}\n")

        new_file.write("[Events]")
        new_file.write("\n{")
        #TODO: Add loop for extracting events
        # 3xTnstruments, band, vocals and LYRICS 
        new_file.write("\n}\n")

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

                sparks_list = []
                for i, this_fret in enumerate(this_diff.frets_on_fire):
                    sp_list = []
                    for this_spark in this_fret.frets_wave:
                        if this_inst_name == "Drums":
                            this_note = i
                        else:
                            this_note = 4 - i
                        
                        #TODO: note modes is:   0x00 NOTE "N", 0x01 "S LEN" STAR, 0x10 HOPO "N 5", 0x20 UP,  0x30 DOWN, 0x02 ???
                        sparks_list.append([this_spark.timing, "N", this_note, this_spark.len])

                        has_sp = this_spark.type & 0x01
                        has_hopo = this_spark.type & 0x10
                        has_strum = this_spark.type & 0x20
                        has_other = this_spark.type & 0x0E  #DEBUG

                        if has_sp:
                            sp_list.append([this_spark.timing, "S", "2", this_spark.len])
                            sparks_list.append([this_spark.timing, "S", "2", this_spark.len])
                            #TODO: combine and unite STAR POWER

                        if has_hopo:
                            sparks_list.append([this_spark.timing, "N", "5", this_spark.len])

                        if has_strum:
                            # TODO: What kind of modifier is this?
                            sparks_list.append([this_spark.timing, "N", "9", this_spark.len])
                            #sparks_list.append([this_spark.timing, "N", "5", this_spark.len])
    
                        if has_other:
                            # TODO: What kind of modifier is there?
                            print("Other fret mod FOUND: " + str(has_other))   #DEBUG
                            #sparks_list.append([this_spark.timing, "N", "10", this_spark.len])
                            #sparks_list.append([this_spark.timing, "N", "5", this_spark.len])

                sorted_sparks = sorted(sparks_list, key=lambda item: item[0])

                for this_sorted_spark in sorted_sparks:
                    new_file.write("\n\t" + str(this_sorted_spark[0]) + " = " + str(this_sorted_spark[1]) + " " + str(this_sorted_spark[2]) + " " + str(this_sorted_spark[3]) )

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
        config.set("song", ";video_start_time" , "3000")
        config.set("song", "delay", "3000") # Verify beats or secs

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
                    song_vol,
                    bpms[0],    # Guitar
                    bpms[1],    # Rhythm
                    bpms[2],    # Drums
                    bpms[3],    # Vocal
                    bpms[4],    # Band
                    speeds[0],  # Guitar-Easy
                    speeds[1],  # Guitar-Norm
                    speeds[2],  # Guitar-Hard
                    speeds[3],  # Rhythm-Easy
                    speeds[4],  # Rhythm-Norm
                    speeds[5],  # Rhythm-Hard
                    speeds[6],  # Drums-Easy
                    speeds[7],  # Drums-Norm
                    speeds[8],  # Drums-Hard
                    speeds[9],  # Vocals
                    res,
                    last_tick,
                    bpm,
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
                    #cmd = cmd + " -y -stats -i "    # DEBUG Verbose 
                    cmd = cmd + "\"" + source_file + "\""
                    cmd = cmd + " -af adelay=3000:all=1 -c:a libvorbis -b:a 320k "     #Skipp 3sec
                    #cmd = cmd + " -c:a libvorbis -b:a 320k " 
                    cmd = cmd + "\"" + dest_file + "\""
                    #print("Command: " + cmd)    # DEBUG
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
                #cmd = cmd + " -y -loglevel -8 -stats -ss 3000ms -i "   # Intro Skip
                cmd = cmd + " -y -loglevel -8 -stats -hwaccel auto -i "
                #cmd = cmd + " -y -stats -i "    # DEBUG Verbose 
                cmd = cmd + "\"" + source_file + "\""
                for i, instrument in enumerate(data_order):
                    audio_in = dest_dir + "\\" + instrument + ".ogg"
                    if os.path.exists(audio_in):
                        cmd = cmd + " -i \"" + audio_in + "\""
                cmd = cmd + " -filter_complex amix=inputs=" 
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
