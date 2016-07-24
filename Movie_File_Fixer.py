# -*- coding: utf-8 -*-
'''
Name: Movie_File_Fixer.py
Author: Blair Gemmer
Version: 20160618

Description: 

Executes a four part movie folder formatting system for a given directory. The system is as follows:

1. [Folderizer] Searches a directory and puts all singleton files into a directory of their namesake.

2. [File_Remover] Removes any files with unwanted extensions like ".txt" or ".dat".

3. [Formatter] Formats all the files and folders in a given directory based on their movie title 
and creates a title directory called "contents.json", which also contains poster information.

4. [Poster_Finder] Reads that "contents.json" file and downloads the poster for each title.

'''
from Folderizer import Folderizer
from Formatter import Formatter
from Poster_Finder import Poster_Finder
from File_Remover import File_Remover

import json
import os

class Movie_File_Fixer():
	def __init__(self, directory=None, extensions=['.nfo', '.dat', '.jpg', '.png', '.txt'], data_files=['contents.json', 'errors.json'], verbose=True):		
		self.folderize(directory=directory, data_files=data_files, verbose=verbose)		
		self.cleanup(directory=directory, extensions=extensions, verbose=verbose)
		self.format(directory=directory, verbose=verbose)
		self.get_posters(directory=directory, data_files=data_files, verbose=verbose)		

	def folderize(self, directory=None, data_files=None, verbose=False):
		'''
		1. Place all single files in folders of the same name.
		'''
		Folderizer(directory=directory, data_files=data_files, verbose=verbose)

	def cleanup(self, directory=None, extensions=None, verbose=False):
		'''
		2. Remove all non-movie files, based on a list of "bad" extensions (i.e., .nfo, .txt, etc)
		'''
		File_Remover(directory=directory, extensions=extensions, verbose=verbose)

	def format(self, directory=None, verbose=False):
		'''
		3. Pull the names of all folders and decide what the title is, based on movie titles in OMDB.
			a. Rename the movie file and folders (i.e., <movie_title> [<year_of_release>])
		'''
		Formatter(directory=directory, verbose=verbose)

	def get_posters(self, directory=None, data_files=None, verbose=False):
		'''
			b. Download the movie poster and name the file poster.<extension> 
			(where <extension> is the original extension of the poster file)
		'''
		contents_file = data_files[0]
		Poster_Finder(directory=directory, contents_file=contents_file, verbose=verbose)

if __name__ == '__main__':
	fake_directory = os.path.join(os.getcwd(), 'test', 'data', 'Fake_Directory')
	directory = fake_directory
	directory = 'J:\\to_sort'		
	Movie_File_Fixer(directory=directory, data_files=['contents.json', 'errors.json'], verbose=False)