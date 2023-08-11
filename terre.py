#!/usr/bin/python
# Python script
# Made by Envido32

import os, re, shutil
import subprocess
import time
import cbr, disc, band

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
data_order = ["head","guitar", "rhythm", "drums", "vocals", "song"]
diff_order = ["easy", "normal", "hard"]
 
print("Working dir:\t [", work_dir, "]")

# Analize files
print(" > Analizing files... < " )
print("Songs dir:\t[", songs_dir ,"]")
os.chdir(songs_dir)

dir_files = os.listdir(songs_dir)
#print("Files in dir:\t",  dir_files)   #DEBUG

chart_files = list()
for filename in dir_files:
    if re.search("\.cbr$", filename):
        chart_files.append(filename)

n = len(chart_files)

# Create log file
if n > 0:
    print("Songs found in dir:\t",  n)
    os.chdir(work_dir)
    new_file = open("songs.csv", "w")
    new_file.write("Artista\tCancion\tDisco\tAño\tSong ID\tBand ID\tDisc ID\tDif:G\tDif:R\tDif:D\tDif:V\tDif:B\n")
    new_file.close()

#print("Disk dir:\t", songs_dir)    #DEBUG

# Output directories
try:
    os.mkdir(raw_dir)
except OSError as error:
    print("Output dir:\t[", raw_dir, "] already exists")
    
# Raw extraction
for filename in chart_files:
    start_song = time.time()
    local = time.strftime("%H:%M:%S", time.localtime(start_song))
    print("Song start: ", local)

    k = chart_files.index(filename) + 1
    
    print("Analizing (", int(k) , "/" , int(n) , ")")   #DEBUG

    os.chdir(songs_dir)
    #working_file = open(filename, "rb")
    #file_id, ext = os.path.splitext(filename)
    #print("File ID = " + file_id)  #DEBUG test Kaitai

    # Read CBR file
    file_cbr = cbr.Cbr.from_file(filename)
    
    # Extract Song ID
    song_id = file_cbr.info.song_id     # Int vble
    song_id = str(hex(song_id)).upper().lstrip('0X')    # String formating
    print("Song ID = " + song_id)  #DEBUG test Kaitai

    # Extract Band ID
    band_id = file_cbr.info.band_id     # Int vble
    band_id = str(hex(band_id)).upper().lstrip('0X')    # String formating
    print("Band ID = " + band_id)  #DEBUG test Kaitai
    
    # Extract Disc ID
    disc_id = file_cbr.info.disc_id     # Int vble
    disc_id = str(hex(disc_id)).upper().lstrip('0X')    # String formating
    print("Disc ID = " + disc_id)  #DEBUG test Kaitai

    # Extract Year
    year = file_cbr.info.year
    print("Year = " + str(year))  #DEBUG test Kaitai
    
    # Extract Song Name
    song_name = str(file_cbr.info.song_name).rstrip('\x00')
    print("Song = " + file_cbr.info.song_name)  #DEBUG test Kaitai

    # Extract Difficulty
    difficulties = file_cbr.tracks.diff_level
    band_diff = int(0)
    for instrument in difficulties:
        band_diff += instrument
    difficulties[4] = int(band_diff / 4)

    print("Diff. Guitar =\t" + str(difficulties[0]))  #DEBUG test Kaitai
    print("Diff. Rythm =\t" + str(difficulties[1]))  #DEBUG test Kaitai
    print("Diff. Drums =\t" + str(difficulties[2]))  #DEBUG test Kaitai
    print("Diff. Vocal =\t" + str(difficulties[3]))  #DEBUG test Kaitai
    print("Diff. Band =\t" + str(difficulties[4]))  #DEBUG test Kaitai

    # Extract Charts
    '''
    # DEBUG test kaitai charts
    chart_heads = list()
    chart_heads.append(file_cbr.tracks.guitar.hdr)
    chart_heads.append(file_cbr.tracks.rhythm.hdr)
    chart_heads.append(file_cbr.tracks.drums.hdr)
    chart_heads.append(file_cbr.tracks.voice.hdr)
    chart_heads.append(file_cbr.tracks.extras.head)

    test_head = file_cbr.tracks.extras.head

    for head_ver in chart_heads:
        print("leng: " + str(len(head_ver)))
        if head_ver == test_head:
            print("Head equal")
        else:
            print("Head diff")
    '''
   
    # Analize Bands
    os.chdir(bands_dir)

    #dir_files = os.listdir(curr_dir) #DEBUG
    #print("Files in dir:", dir_files) #DEBUG

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

    #TODO make CH compatible
    '''
    for chart in charts:
        i = charts.index(chart)
        new_file = open("chart_" + data_order[i] + ".cbr", "wb")
        if i > 0:
            new_file.write(chart_head)
        new_file.write(chart)
        new_file.close()
    '''

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

    new_file = open("events.csv", "w")
    
    new_file.write("[GUITAR]\t\t\t[RHYTHM]\t\t\t[DRUMS]\t\t\t[VOICE]\t\t\t[EXTRAS]\t\t\t\n")
    new_file.write("[val]\t[len]\t[num]\t[val]\t[len]\t[num]\t[val]\t[len]\t[num]\t[val]\t[len]\t[num]\t[val]\t[len]\t[num]\t\n")

    print("GUITAR header len:" + str(len(file_cbr.tracks.guitar.hdr.events)))
    print("RHYTHM header len:" + str(len(file_cbr.tracks.rhythm.hdr.events)))
    print("DRUMS header len:" + str(len(file_cbr.tracks.drums.hdr.events)))
    print("VOICE header len:" + str(len(file_cbr.tracks.vocals_with_extras.hdr.events)))
    print("EXTRAS header len:" + str(len(file_cbr.tracks.extras.events)))


    head_lens = [ len(file_cbr.tracks.guitar.hdr.events),  len(file_cbr.tracks.rhythm.hdr.events),  len(file_cbr.tracks.drums.hdr.events),  len(file_cbr.tracks.vocals_with_extras.hdr.events),  len(file_cbr.tracks.extras.events) ]
    largest_number = head_lens[0]
    for number in head_lens:
        if number > largest_number:
            largest_number = number
    
    print("BIGGER header len:" + str(largest_number))  # DEBUG
    
    guitar_lines = list()
    for block in file_cbr.tracks.guitar.hdr.events:
        guitar_lines.append(str(block.val) + "\t" + str(block.cont) + "\t" + str(block.pos) + "\t" )
    
    add_head = largest_number - len(file_cbr.tracks.guitar.hdr.events)
    while add_head:
        #guitar_lines.append("g\tg\tg\t")    # DEBUG
        guitar_lines.append("\t\t\t")
        add_head-=1
    
    rhythm_lines = list()
    for block in file_cbr.tracks.rhythm.hdr.events:
        rhythm_lines.append(str(block.val) + "\t" + str(block.cont) + "\t" + str(block.pos) + "\t" )
    
    add_head = largest_number - len(file_cbr.tracks.rhythm.hdr.events)
    while add_head:
        #rhythm_lines.append("r\tr\tr\t")    # DEBUG
        rhythm_lines.append("\t\t\t")
        add_head-=1

    drums_lines = list()
    for block in file_cbr.tracks.drums.hdr.events:
        drums_lines.append(str(block.val) + "\t" + str(block.cont) + "\t" + str(block.pos) + "\t" )
        
    add_head = largest_number - len(file_cbr.tracks.drums.hdr.events)
    while add_head:
        #drums_lines.append("d\td\td\t") # DEBUG
        drums_lines.append("\t\t\t")
        add_head-=1
    
    voice_lines = list()
    for block in file_cbr.tracks.vocals_with_extras.hdr.events:
        voice_lines.append(str(block.val) + "\t" + str(block.cont) + "\t" + str(block.pos) + "\t" )

    add_head = largest_number - len(file_cbr.tracks.vocals_with_extras.hdr.events)
    while add_head:
        #voice_lines.append("v\tv\tv\t") # DEBUG
        voice_lines.append("\t\t\t")
        add_head-=1
    
    extras_lines = list()
    for block in file_cbr.tracks.extras.events:
        extras_lines.append(str(block.val) + "\t" + str(block.cont) + "\t" + str(block.pos) + "\t" )

    add_head = largest_number - len(file_cbr.tracks.extras.events)
    while add_head:
        #extras_lines.append("e\te\te\t")    # DEBUG
        extras_lines.append("\t\t\t")
        add_head-=1
    
    all_lines = list()
    i=0
    for line in extras_lines:
        try:
            all_lines.append(guitar_lines[i] + rhythm_lines[i] + drums_lines[i] + voice_lines[i] + extras_lines[i] + "\n" )
        except:
            print("DEBUG i muy grande") # DEBUG
        i+=1

    new_file.writelines(all_lines)
    new_file.close()

    # Instruments charing manual analisis
    new_file = open("charts.csv", "w")
    new_file.write("[GUITAR]\t\t\t\t\t\t\t\t\t[RHYTHM]\t\t\t\t\t\t\t\t\t[DRUMS]\t\t\t\t\t\t\t\t\t\n")
    new_file.write("[easy]\t\t\t[norm]\t\t\t[hard]\t\t\t[easy]\t\t\t[norm]\t\t\t[hard]\t\t\t[easy]\t\t\t[norm]\t\t\t[hard]\t\t\t\n")
    new_file.write("[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t[lo]\t[me]\t[hi]\t\n")

    chart_lens = list()
    chart_lens.append(len(file_cbr.tracks.guitar.easy.song))
    chart_lens.append(len(file_cbr.tracks.guitar.norm.song))
    chart_lens.append(len(file_cbr.tracks.guitar.hard.song))

    chart_lens.append(len(file_cbr.tracks.rhythm.easy.song))
    chart_lens.append(len(file_cbr.tracks.rhythm.norm.song))
    chart_lens.append(len(file_cbr.tracks.rhythm.hard.song))

    chart_lens.append(len(file_cbr.tracks.drums.easy.song))
    chart_lens.append(len(file_cbr.tracks.drums.norm.song))
    chart_lens.append(len(file_cbr.tracks.drums.hard.song))

    largest_number = chart_lens[0]
    for number in chart_lens:
        if number > largest_number:
            largest_number = number
    
    print("BIGGER diff len:" + str(largest_number))  # DEBUG
    
    print("GUITAR easy len:" + str(int(len(file_cbr.tracks.guitar.easy.song)/3)))
    print("GUITAR norm len:" + str(int(len(file_cbr.tracks.guitar.norm.song)/3)))
    print("GUITAR hard len:" + str(int(len(file_cbr.tracks.guitar.hard.song)/3)))

    print("RHYTHM easy len:" + str(int(len(file_cbr.tracks.rhythm.easy.song)/3)))
    print("RHYTHM norm len:" + str(int(len(file_cbr.tracks.rhythm.norm.song)/3)))
    print("RHYTHM hard len:" + str(int(len(file_cbr.tracks.rhythm.hard.song)/3)))

    print("DRUMS easy len:" + str(int(len(file_cbr.tracks.drums.easy.song)/3)))
    print("DRUMS norm len:" + str(int(len(file_cbr.tracks.drums.norm.song)/3)))
    print("DRUMS hard len:" + str(int(len(file_cbr.tracks.drums.hard.song)/3)))

    guitar_easy_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.guitar.easy.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            guitar_easy_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.guitar.easy.song)
    add_diff /= 3
    while add_diff:
        #guitar_easy_lines.append("ge\tge\tge\t")    # DEBUG
        guitar_easy_lines.append("\t\t\t")
        add_diff-=1

    guitar_norm_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.guitar.norm.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            guitar_norm_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.guitar.norm.song)
    add_diff /= 3
    while add_diff:
        #guitar_norm_lines.append("gn\tgn\tgn\t")    # DEBUG
        guitar_norm_lines.append("\t\t\t")
        add_diff-=1

    guitar_hard_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.guitar.hard.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            guitar_hard_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.guitar.hard.song)
    add_diff /= 3
    while add_diff:
        #guitar_hard_lines.append("gh\tgh\tgh\t")    # DEBUG
        guitar_hard_lines.append("\t\t\t")
        add_diff-=1

    rhythm_easy_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.rhythm.easy.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            rhythm_easy_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.rhythm.easy.song)
    add_diff /= 3
    while add_diff:
        #rhythm_easy_lines.append("re\tre\tre\t")    # DEBUG
        rhythm_easy_lines.append("\t\t\t")
        add_diff-=1

    rhythm_norm_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.rhythm.norm.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            rhythm_norm_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.rhythm.norm.song)
    add_diff /= 3
    while add_diff:
        #rhythm_norm_lines.append("rn\trn\trn\t")    # DEBUG
        rhythm_norm_lines.append("\t\t\t")
        add_diff-=1

    rhythm_hard_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.rhythm.hard.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            rhythm_hard_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.rhythm.hard.song)
    add_diff /= 3
    while add_diff:
        #rhythm_hard_lines.append("rh\trh\trh\t")    # DEBUG
        rhythm_hard_lines.append("\t\t\t")
        add_diff-=1

    drums_easy_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.drums.easy.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            drums_easy_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.drums.easy.song)
    add_diff /= 3
    while add_diff:
        #drums_easy_lines.append("de\tde\tde\t")    # DEBUG
        drums_easy_lines.append("\t\t\t")
        add_diff-=1

    drums_norm_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.drums.norm.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            drums_norm_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.drums.norm.song)
    add_diff /= 3
    while add_diff:
        #drums_norm_lines.append("dn\tdn\tdn\t")    # DEBUG
        drums_norm_lines.append("\t\t\t")
        add_diff-=1

    drums_hard_lines = list()
    i=0
    aux_line = ""
    for block in file_cbr.tracks.drums.hard.song:
        aux_line = aux_line + str(block) + "\t"
        i+=1
        if i%3 == 0:
            drums_hard_lines.append(aux_line)
            aux_line = ""    
    
    add_diff = largest_number - len(file_cbr.tracks.drums.hard.song)
    add_diff /= 3
    while add_diff:
        #drums_hard_lines.append("dh\tdh\tdh\t")    # DEBUG
        drums_hard_lines.append("\t\t\t")
        add_diff-=1

    all_lines = list()
    i=0
    for line in guitar_easy_lines:
        try:
            all_lines.append(guitar_easy_lines[i] + guitar_norm_lines[i] + guitar_hard_lines[i] + rhythm_easy_lines[i] + rhythm_norm_lines[i] + rhythm_hard_lines[i] + drums_easy_lines[i] + drums_norm_lines[i] + drums_hard_lines[i] + "\n" )
        except:
            print("DEBUG i muy grande") # DEBUG
        i+=1

    new_file.writelines(all_lines)
    new_file.close()
    

    # Save metadata
    new_file = open("song.ini", "w")
    new_file.write("[song]")
    new_file.write("\nartist = " + band_name)
    new_file.write("\nname = " + song_name)
    new_file.write("\nalbum = " + disc_name)
    new_file.write("\nyear = " + str(year))
    new_file.write("\ndiff_guitar = " + str(difficulties[0]))
    new_file.write("\ndiff_bass = " + str(difficulties[1]))
    new_file.write("\ndiff_vocals = " + str(difficulties[2]))
    new_file.write("\ndiff_drums = " + str(difficulties[3]))
    new_file.write("\ndiff_band = " + str(difficulties[4]))
    new_file.write("\nicon = erdtv")
    new_file.write("\ngenre = Rock Argentino")
    new_file.write("\ncharter = Next Level")
    new_file.write("\nbanner_link_a = http://www.elrockdetuvida.com/website/index.php")
    new_file.write("\nlink_name_a = Homepage")
    new_file.write("\nloading_phrase = Viví la experiencia de interpretar los temas de tus bandas favoritas del rock nacional.")
    new_file.write("\n;video_start_time=3000")
    new_file.write("\ndelay=3000")
    new_file.write("\n")
    new_file.close()

    # Save to log
    os.chdir(work_dir)
    new_file = open("songs.csv", "a")
    new_file.write(band_name + "\t")
    new_file.write(song_name + "\t")
    new_file.write(disc_name + "\t")
    new_file.write(str(year) + "\t")
    new_file.write(song_id + "\t")
    new_file.write(band_id + "\t")
    new_file.write(disc_id + "\t")
    new_file.write(str(difficulties[0]) + "\t") # Guitar
    new_file.write(str(difficulties[1]) + "\t") # Rythm
    new_file.write(str(difficulties[2]) + "\t") # Drums
    new_file.write(str(difficulties[3]) + "\t") # Vocal
    new_file.write(str(difficulties[4]) + "\n") # Band
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
    
# Convert to Clone Hero (need FFMPEG)
#convert = input("Convertir a Clone Hero? (esto puede tomar bastante tiempo) [y/n]: ")[0].upper()
#convert = 'Y'  #DEBUG
convert = 'N'  #DEBUG
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
            #cmd = cmd + " -y -stats -i "    #DEBUG Verbose 
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
            #cmd = cmd + " -y -stats -i "    #DEBUG Verbose 
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
