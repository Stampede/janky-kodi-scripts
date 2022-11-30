#!/usr/bin/env python

# movieFolderRename.py - Nov. 30, 2022 edition
# Start this script from a directory containing movie files and movie folders.
# It will try to determine the title & year of the movie and ask you to confirm.
# If you confirm, it will rename the folder to "Movie Title (Year)"
# In the case of movie files that are not already in folders, it will create the folder
# and move the video file into the new folder.
# When it's over, it will put a file called "Rename Report.txt" in the directory.
# Check over that file for skipped items. This script catches about 85% correctly, but
# you'll probably have to do some manual renaming.



import os, re, shutil
from pathlib import Path
import pyinputplus as pyip




def suggest_new_name(old_name, title, year, isFile=False):
    if isFile:
        print()
        print(old_name, 'is a file.')
        print("I'll create a new directory and move the video file into it, if you approve of the folder name.")

    new_name = title + f' ({year})'
    if new_name == old_name:
        return None

    print('Control-C to quit.')
    print()
    print('Original name:'.ljust(26), old_name)
    print('Suggested folder name:'.ljust(26), new_name)
    print()
    if pyip.inputYesNo(prompt='Approve? ', default='no') == 'no':
        rejected_suggestions.append((old_name, new_name))
        print('Suggestion rejected.\n')
        return None
    else:
        if isFile:
            os.mkdir(os.path.join('Renamed Folders', new_name))
            shutil.move(old_name, Path('Renamed Folders') / new_name)
            print(f"{old_name} moved into folder {new_name}.")
        elif Path(old_name).is_dir():
            shutil.move(old_name, Path('Renamed Folders') / new_name)
            print(f"{old_name} has been renamed to {new_name} and placed in the 'Renamed Folders' directory.")

Path.mkdir(Path.cwd() / 'Renamed Folders', exist_ok=True)
directory_contents = os.listdir()

name_yearREGEX = re.compile(r'([A-Z].*[a-z].*?(I{1,3}|\d)?).?((19\d{2})|(20[0-2]\d))') # Group 1 is the title, Group 3 is the year

skipped_items, rejected_suggestions = ([], [])

for item in directory_contents:
    if os.path.isfile(item): stripped_dots = re.sub(r'\.', ' ', Path(item).stem)
    elif os.path.isdir(item): stripped_dots = re.sub(r'\.', ' ', item)
    
    mo = name_yearREGEX.search(stripped_dots)
    if mo == None:
        skipped_items.append(item + '\n')
        continue
    
    if (Path.cwd() / item).is_file(): suggest_new_name(item, mo.group(1).strip(), mo.group(3), isFile=True)
    elif (Path.cwd() / item).is_dir(): suggest_new_name(item, mo.group(1).strip(), mo.group(3))
    else: raise Exception(f"I can't tell if {item} is a file or a directory!")

with open('Rename Report.txt', 'w') as f:
    f.write('Could not find a title and year for the following items. You need to handle them manually.\n')
    f.writelines(skipped_items)
    f.write('\n' + ('*-+' * 20) + '\n')
    f.write('You rejected these suggestions. Handle them manually.\n')
    f.write('REJECTED:' + ('\t' * 3) + 'ORIGINAL NAME:\n')
    for old, new in rejected_suggestions:
        f.write(new)
        f.write(('\t' * 3) + old + '\n')

print('Finished. Skipped files are reported in this directory.')

##############################################################################################

'''Version history:
Nov. 28, 2022 15:46     This worked well enough. Had some problems with numbers in movie titles,
                        probably because of regex squirelliness.

Nov. 28, 2022 23:29     Added a line to skip processing if the new name is the same as the old name,
                        this was a PITA when I had it parsing through a directory with many names
                        already formatted correctly.

'''