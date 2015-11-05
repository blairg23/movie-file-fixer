# Description
Iterates through a directory of movie files and formats the filenames, as well as downloads the movie poster. 

# Algorithm
1. Search given directory.
    a. Place all single files in folders of same name. - [Folderizer.py]    
    b. Collect all names of folders (including the recently created ones).
2. Pull the names of all folders and decide what the title is, based on movie titles.
    a. Rename the movie file and folder (i.e., <movie_title> [<year_of_release>])- [Formatter.py]
    b. Download the movie poster and name the file poster.png - [Poster_Finder.py]
3. Folder Cleanup.
    a. Remove non-movie files, based on a list of "bad" extensions (i.e., .nfo, .txt, etc) - [File_Remover.py]