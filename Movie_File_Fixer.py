# -*- coding: utf-8 -*-
'''
Name: Movie_File_Fixer.py
Author: Blair Gemmer
Version: 20151122

Description: 

Executes a four part movie folder formatting system for a given directory. The system is as follows:

1. [Folderizer] Searches a directory and puts all singleton files into a directory of their namesake.

2. [File_Remover] Removes any files with unwanted extensions like ".txt" or ".dat".

3. [Formatter] Formats all the files and folders in a given directory based on their movie title 
and creates a title directory called "titles.json", which also contains poster information.

4. [Poster_Finder] Reads that "titles.json" file and downloads the poster for each title.

'''
from Folderizer import Folderizer
from Formatter import Formatter
from Poster_Finder import Poster_Finder
from File_Remover import File_Remover

from Helper_Functions import *
import json

class Movie_File_Fixer():
	def __init__(self, directory=None, verbose=True):
		self.folderize(directory=directory, verbose=verbose)
		self.cleanup(directory=directory, verbose=verbose)
		self.format(directory=directory, verbose=verbose)
		self.get_posters(directory=directory, verbose=verbose)		

	def folderize(self, directory=None, verbose=False):
		'''
		1. Place all single files in folders of the same name.
		'''
		Folderizer(directory=directory, verbose=verbose)

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

	def get_posters(self, directory=None, verbose=False):
		'''
			b. Download the movie poster and name the file poster.<extension> 
			(where <extension> is the original extension of the poster file)
		'''
		Poster_Finder(directory=directory, verbose=verbose)




if __name__ == '__main__':
	Movie_File_Fixer(directory=join(getcwd(), 'data', 'Fake_Directory'), verbose=True)