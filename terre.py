#!/usr/bin/python
# Python script
# Made by Envido32

import os, re, shutil
import subprocess
import time
import cbr, disc, band
import csv, configparser

# Config Constants 
data_order = ["head","guitar", "rhythm", "drums", "vocals", "song"]
inst_order = ["guitar", "rhythm", "drums", "vocals", "extras"]
diff_order = ["easy", "norm", "hard"]

def ExtractEvents(file_cbr: cbr.Cbr):
    head_lens = []
    for this_inst in inst_order:
        file_name = "events_" + this_inst + ".csv"
        event_file = open(file_name, "w", newline="")
        csv_writer = csv.writer(event_file)
        data_in = [ "count", "type", "DIFF"]
        csv_writer.writerow(data_in)
        
        match this_inst:
            case "guitar":
                inst_events = file_cbr.tracks.guitar.hdr.events
            case "rhythm":
                inst_events = file_cbr.tracks.rhythm.hdr.events
            case "drums":
                inst_events = file_cbr.tracks.drums.hdr.events
            case "vocals":
                try:                    
                    inst_events = file_cbr.tracks.vocals_with_extras.hdr.events
                except:
                    inst_events = file_cbr.tracks.vocals_no_extras.hdr.events
            case "extras":
                try:    
                    inst_events = file_cbr.tracks.extras.events
                except:
                    inst_events = []
            case _:
                inst_events = []

        head_lens.append(len(inst_events))
        print(this_inst + " header len: " + str(int(len(inst_events))))
        
        csv_rows = []
        aux = 0
        i = 0
        bar_prev = -1
        for block in inst_events:
            if block.count == bar_prev:
                i += 1
                last_bar = " "
            else:
                last_bar = str(i)
                i = 0
            bar_prev = block.count
            #data_in = [ block.foo, block.bar, block.pos, (block.foo - aux), i, last_bar]
            data_in = [ format(block.count, "06X"), block.type, (block.count - aux)]
            aux = block.count
            csv_rows.append(data_in)

        csv_writer.writerows(csv_rows)
        #data_in = ["DATOS", max_bar, max_pos]
        event_file.close()

    # TODO: Compare event files

    largest_number = head_lens[0]
    for number in head_lens:
        if number > largest_number:
            largest_number = number
    
    print(" > BIGGER header len:" + str(largest_number))  # DEBUG

def ExtractCharts(file_cbr: cbr.Cbr):
    notes_len = []
    for this_inst in inst_order:
        for this_diff in diff_order:
            file_name = "charts_" + this_inst + "_" + this_diff + ".csv"
            chart_file = open(file_name, "w", newline="")
            csv_writer = csv.writer(chart_file)
            data_in = [ "foo", "bar", "pos" ]
            csv_writer.writerow(data_in)
            
            match this_inst:
                case "guitar":
                    notes_inst = file_cbr.tracks.guitar
                case "rhythm":
                    notes_inst = file_cbr.tracks.rhythm
                case "drums":
                    notes_inst = file_cbr.tracks.drums
                case "vocals":
                    try:
                        notes_inst = file_cbr.tracks.vocals_with_extras
                    except: 
                        notes_inst = file_cbr.tracks.vocals_no_extras
                case _:
                    notes_inst = []

            if notes_inst:
                if this_inst == "vocals":
                    notes = notes_inst.elements
                    addrs = notes_inst.pts_wave
                else:
                    match this_diff:
                        case "easy":
                            notes = notes_inst.easy.song
                        case "norm":
                            notes = notes_inst.norm.song                        
                        case "hard":
                            notes = notes_inst.hard.song
                        case _:
                            notes = []
                notes_len.append(len(notes))

                # TODO: analize notes_inst.lyrics for vocals

                print(this_inst + " " + this_diff + " len: " + str(int(len(notes))))
                
                csv_rows = []
                j = 0
                for block in notes:
                    try:
                        data_in = [ block.foo, block.bar, block.pos ]
                    except:
                        if block.water[1] != block.water[5]:
                            print("Dif found in voice") # DEBUG
                        if block.water[2] != block.water[7]:
                            print("Dif found in voice") # DEBUG
                        if block.water[4] != block.water[6]:
                            print("Dif found in voice") # DEBUG
                        data_in = [ addrs[j], block.next_pt - 16 ]
                        aux = addrs[j] - block.next_pt + 28
                        if ( aux ):
                            print("Dif addr fond!") # DEBUG
                        for i in range(5):
                            data_in.append(block.water[i])
                        j += 1
                    csv_rows.append(data_in)
                
            csv_writer.writerows(csv_rows)
            chart_file.close()

    largest_number = notes_len[0]
    for number in notes_len:
        if number > largest_number:
            largest_number = number
    
    print(" > BIGGER diff len:" + str(largest_number))  # DEBUG

if __name__ == "__main__":

    start_time = time.time()

    print(" >>> EXTRACTOR TODO EL ROCK (RECARGADO) <<< ")

    localtime = time.localtime(start_time)
    local = time.strftime("%H:%M:%S", localtime)
    print("Start time: ", local)

    #disc_dir = input("Elegi la unidad del disco ERDTV: ")[0].upper() + ":"
    disc_dir = "E:" # DEBUG
    #mozart_dir = disc_dir + "\\install\\data\\mozart"
    mozart_dir = "D:\\Games\\Rythm\\ERDTV\\Mozart"
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
                    "Dif:B"
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
    for filename in cbr_files:
        start_song = time.time()
        local = time.strftime("%H:%M:%S", time.localtime(start_song))
        print("Song start: ", local)

        k = cbr_files.index(filename) + 1
        
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
        for audio in audio_data:
            i = audio_data.index(audio)
            data_order[i]
            new_file = open(data_order[i] + ".flac", "wb")
            new_file.write(flac_head)
            new_file.write(audio)
            new_file.close()

        # Copy preview
        source = songs_dir + "\\" + song_id
        dest = new_song_dir
        #print("Copying preview...")
        try:
            shutil.copyfile(source + ".prv", dest  + "\\preview.wav")
        except:
            print("File [ ", dest,  "\\preview.wav ] already exists")

        # Copy video (slow)
        #print("Copying video...")
        try:
            shutil.copyfile(source + ".vid", dest  + "\\video.asf")
        except:
            print("File [ ", dest,  "\\video.asf ] already exists")

        # Copy icon
        # TODO extract from Disk (.ico to .png)
        #print("Copying icon...")
        source = work_dir
        dest = new_song_dir
        try:
            shutil.copyfile(source + "\\erdtv.png", dest  + "\\erdtv.png")
        except:
            print("File [ ", dest,  "\\erdtv.png ] already exists")

        # Save Kaitai Log
        # COMMON HEADER

        ExtractEvents(file_cbr)
        ExtractCharts(file_cbr)

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

        new_file = open("song.ini", "w")
        config.write(new_file)
        new_file.close()

        # Save to log
        os.chdir(work_dir)
        csv_name = "songs.csv"
        new_file = open(csv_name, "a", newline="")
        csv_writer = csv.writer(new_file)
        data_in =  [ band_name,
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
                     difficulties[4] # Band
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
    #convert = 'Y'  # DEBUG
    convert = 'N'  # DEBUG
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
        n = len(songs_list)

        # Loof for each song
        for this_song in songs_list:
            i = songs_list.index(this_song) + 1
            print(" >> Converting (", int(i) , "/" , int(n) , "): ", this_song) 

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
            #print("Copying album...")
            try:
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
            #print("Copying icon...")
            try:
                copy_file = "\\erdtv.png"
                source_file = source_dir + copy_file
                dest_file = dest_dir + copy_file
                shutil.copyfile(source_file, dest_file)
            except:
                print("File [ ", dest_file, " ] already exists")

            # Copy metadata file
            #print("Copying metadata...")
            try:
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
                j = 0
                for instrument in data_order:
                    audio_in = dest_dir + "\\" + instrument + ".ogg"
                    if os.path.exists(audio_in):
                        j+=1
                        cmd = cmd + " -i \"" + audio_in + "\""
                cmd = cmd + " -filter_complex amix=inputs=" 
                cmd = cmd + str(int(j)) 
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
            eta_time = time.gmtime((total_tm / i ) * (n - i))
            print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))

    total_tm = time.time() - start_time
    total = time.strftime("%H:%M:%S", time.gmtime(total_tm))
    print("All tasks took: " , total)
