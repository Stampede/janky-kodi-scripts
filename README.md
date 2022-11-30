# Janky Kodi Scripts
Kodi is fussy about video file names and formats. These scripts aim to make organizing for Kodi easier.
* Tested on Linux so far.
* They are janky, so they usually ask for user confirmation before writing anything.
* They are janky so back your files up before using.
* Once I have my library organized, I will not be using these scripts often, so they are not perfect, but much better than nothing.
* No promises; no warranties. Back things up!

## movieFolderRename.py
### What it does

I had a messy collection of movies with all sorts of garbage in the filenames. [Kodi likes it very much](https://kodi.wiki/view/Naming_video_files/Movies#Naming) if you put the movies in a folder and format the folder name like: "MOVIE TITLE (YYYY)."

This script will examine the filenames, and try to determine the title and year (assuming they are contained somewhere in the filename). It will then rename the folder to comply with Kodi's demands.

In case it finds just a video file and no folder, then it will still try to guess, then create a folder and move that movie into it.

When finished, it will save a file called "Rename Report.txt." That file will list anything that was skipped by the program, or suggestions rejected by the user.
### How to use
CD into the directory with your unformatted folder names and filenames. Then run the script.

It's not perfect, so it asks for confirmation each time before doing anything.
It's not perfect, so make a backup before running it.
In my experience, it works correctly on 85-90% of files. The rest you still have to do manually.

## nfoGrabber.py
Even with good folder names, sometimes Kodi can't find the correct movie metadata. You can specify what data to scrape for your movie by [designating a target URL](https://kodi.wiki/view/NFO_files/Parsing#Create) for the scraper.

This script will parse your `kodi.log` file and launch a web browser window to search for that movie title on themoviedb.org. Your job is to look at the movie title on your machine, then choose the correct one from the movie DB search. Right click --> "Copy Link Address" on the movie. nfoGrabber.py will detect that you copied something to your clipboard and will save that URL to a movie.nfo file in the correct folder. Then the Kodi scraper will work.

The script asks for confirmation before writing anything in case you copied the wrong thing to the clipboard.

### Assumptions: 
* You already have your folders named properly (as with the movieFolderRename.py script above).
* A file named `kodi.log` exists in the same directory you are in when you run the script.

[Where to find the Kodi log](https://kodi.wiki/view/Log_file#Log_file_location)

### Recommended usage procedure:
1) Shut down Kodi
2) Delete existing [Kodi logs](https://kodi.wiki/view/Log_file#Log_file_location)
3) Start up Kodi, and have it re-scan your library. You want it to fail at scraping movie info.
4) Shut down Kodi
5) Read through the new `kodi.log` file and find the part where it couldn't scrape the info. Look for lines that say: `WARNING <general>: No information found for item...`  and then followed by a file path.
6) You need to put the filepath leading up to the movie files into the script itself. Open the script in a text editor and towards the beginning, look for the line that says `pathREGEX = ...` I left a template in the script for you to use. Replace the `<` and `>` and everything in between them with the path to your movie folders. 
7) You'll need to comment out or delete the `pathREGEX` that's already there since it's unique to my computer.
8) `cd` into the directory where the log is stored.
9) Run the script.

Example: if your movie library folder looks like this:
```
'/some/path/going/to/library/Terminator 2 Judgement Day (1991)'
'/some/path/going/to/library/Fried Green Tomatoes (1991)'
```
Then you would plug in `/some/path/going/to/library/` to the REGEX template.

Between these instructions and the comments I put in the script itself, hopefully you can figure it out.
