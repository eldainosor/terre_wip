#!/usr/bin/python
# Python script
# Made by Envido32

import time
from terre_ext import *

# Config Constants 
#debug = True       #DEBUG
debug = False       #DEBUG
#const_res = 480     #Like RB
#const_res = 192    #Like GH

if __name__ == "__main__":

    print(" >>> EXTRACTOR TODO EL ROCK (RECARGADO) <<< ")

    cfg = Settings(debug)
    pl = Playlist(cfg, debug)
    pl.log_start(cfg, debug)
    # Create log file
    if len(pl.files) > 0:
        print("Songs found in dir:\t",  len(pl.files))   
    else:
        print("<ERROR>: No songs found in dir")

    # Raw extraction
    for k, filename in enumerate(pl.files):
        k += 1
        n = len(pl.files)
        print("Analizing (", int(k) , "/" , int(n) , ")")   # DEBUG

        this_song = Song(cfg, filename, debug)
        pl.append(this_song)

        this_song.create_metadata(debug)
        this_song.extract_charts(cfg, debug)
        this_song.extract_icon(cfg, debug)
        this_song.extract_preview(cfg, debug)
        this_song.extract_audio(cfg, debug)
        this_song.extract_album(cfg, debug)
        this_song.extract_background(cfg, debug)
        this_song.extract_video(cfg, debug)

        #this_song.convert_charts(cfg, debug)    #DEBUG

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
            this_song.convert_charts(cfg, debug)
            this_song.convert_icon(debug)
            this_song.convert_preview(cfg, debug)
            this_song.convert_audio(cfg, debug)
            this_song.convert_album(debug)
            this_song.convert_background(debug)
            this_song.convert_video(cfg, debug)

            # Show time and ETA
            elapsed_tm = time.time() - start_song
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_tm))
            print("This song took:\t" , elapsed)
            total_tm = cfg.print_elapsed_time()
            eta_time = time.gmtime((total_tm / k ) * (n - k))
            print("ETA:\t" , time.strftime("%H:%M:%S", eta_time))

    cfg.print_elapsed_time()
    