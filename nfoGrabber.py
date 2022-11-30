#!/usr/bin/env python
# nfoGrabber.py - Nov. 29, 2022 01:55 Edition
# This script parses Kodi error log for movies that it couldn't scrape. It then
# auto-launches a web browser and searches for the movie title on themoviedb.org.
# User copies URL for the correct movie to the clipboard and the script will
# use that URL and save a movie.nfo file in the correct folder. Next time Kodi scans
# the library, it will download the correct metadata.

# Script assumes your folders are named in the "Title (Year)" format already.
# No promises! Back your shit up before running this!
# You'll need to comment out my "pathREGEX." make your own for wherever you store your files.

import webbrowser, re, pyperclip, os, time
import pyinputplus as pyip

pathREGEX = re.compile(r"'(/mnt/DnM/Media Library/Videos/Movies/((.+)\(\d{4}\).?)/)")
# REGEX TEMPLATE: type the root path leading to your movie folder as seen in the Kodi log:
# pathREGEX = re.compile(r"'<PUT ROOT PATH HERE. INCLUDE TRAILING SLASH>((.+)\(\d{4}\).?)/)")

# Group 1 is the absolute path to the parent directory where the .nfo will go
# Group 2 is "Movie Title (YYYY)"
# Group 3 is just the movie title (for use in web searching)

warning_string = 'WARNING <general>: No information found for item'

def search(title):
    base_url = 'https://www.themoviedb.org/search?query='
    search_string = re.sub(r' ', '+', title.strip())
    webbrowser.open(base_url + search_string)

def wait_for_clip():
    cboard_checkpoint = pyperclip.paste()
    while pyperclip.paste() == cboard_checkpoint:
        time.sleep(0.25)
    return pyperclip.paste()

with open('kodi.log', 'r') as f:
    log = f.readlines()

for entry in log:
    if warning_string not in entry:
        continue
    
    URL_chosen = False
    mo = pathREGEX.search(entry)
    search(mo.group(3))

    while not URL_chosen:
        print()
        print(f'Copy the correct URL for {mo.group(2)} to the clipboard.')
        movie_url = wait_for_clip()
        print(f'URL: {movie_url}')
        conf = pyip.inputYesNo(prompt='Agree? (Enter blank to skip this file.) ', blank=True)

        if conf == '':
            break
        elif conf == 'yes': URL_chosen = True
    
    if not URL_chosen: continue

    nfo_path = os.path.join(mo.group(1), 'movie.nfo')
    with open(nfo_path, 'w') as f:
        f.write(movie_url)
    