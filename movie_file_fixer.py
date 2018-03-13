# -*- coding: utf-8 -*-
'''
Name: movie_file_fixer.py
Author: Blair Gemmer
Version: 20170604

Description: 

Executes a five part movie folder formatting system for a given directory. The system is as follows:

1. [Folderizer] Searches a directory and puts all singleton files into a directory of their namesake.

2. [File_Remover] Removes any files with unwanted extensions like ".txt" or ".dat".

3. [Formatter] Formats all the files and folders in a given directory based on their movie title 
and creates a title directory called "contents.json", which also contains poster information.

4. [Poster_Finder] Reads that "contents.json" file and downloads the poster for each title.

5. [Subtitle_Finder] Reads the "contents.json" file and downloads the subtitle for each title.

'''

import os

from file_remover import FileRemover
from folderizer import Folderizer
from formatter import Formatter
from poster_finder import PosterFinder
from subtitle_finder import SubtitleFinder


class MovieFileFixer():
    def __init__(self, directory=None, extensions=['.nfo', '.dat', '.jpg', '.png', '.txt'], data_files=['contents.json', 'errors.json'], verbose=True):
        self.folderize(directory=directory, data_files=data_files, verbose=verbose)
        self.cleanup(directory=directory, extensions=extensions, verbose=verbose)
        self.format(directory=directory, verbose=verbose)
        self.get_posters(directory=directory, data_files=data_files, verbose=verbose)
        self.get_subtitles(directory=directory, data_files=data_files, verbose=verbose)

    def folderize(self, directory=None, data_files=None, verbose=False):
        '''
        1. Place all single files in folders of the same name.
        '''
        Folderizer(directory=directory, data_files=data_files, verbose=verbose)

    def cleanup(self, directory=None, extensions=None, verbose=False):
        '''
        2. Remove all non-movie files, based on a list of "bad" extensions (i.e., .nfo, .txt, etc)
        '''
        FileRemover(directory=directory, extensions=extensions, verbose=verbose)

    def format(self, directory=None, verbose=False):
        '''
        3. Pull the names of all folders and decide what the title is, based on movie titles in OMDb API.
            a. Rename the movie file and folders (i.e., <movie_title> [<year_of_release>])
        '''
        Formatter(directory=directory, verbose=verbose)

    def get_posters(self, directory=None, data_files=None, verbose=False):
        '''
        4. Download the movie poster and name the file poster.<extension>
        (where <extension> is the original extension of the poster file)
        '''
        contents_file = data_files[0]
        PosterFinder(directory=directory, contents_file=contents_file, verbose=verbose)

    def get_subtitles(self, directory=None, data_files=None, language='en', verbose=False):
        '''
        5. Download the movie subtitles and name the file <language>_subtitles.srt
        '''
        contents_file = data_files[0]
        SubtitleFinder(directory=directory, contents_file=contents_file, language=language, verbose=verbose)


if __name__ == '__main__':
    fake_directory = os.path.join(os.getcwd(), 'test', 'data', 'Fake_Directory')
    directory = fake_directory
    directory = os.path.join(os.getcwd(), 'input')
    # directory = "C:/Users/Neophile/Desktop/sandboxes/python/movie-file-fixer/input/"
    MovieFileFixer(directory=directory, data_files=['contents.json', 'errors.json'], verbose=False)
