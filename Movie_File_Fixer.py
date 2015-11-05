from Folderizer import Folderizer
from Formatter import Formatter
from Poster_Finder import Poster_Finder

from Helper_Functions import *
import json

class Movie_File_Fixer():
	def __init__(self, directory=None, verbose=True):
		folderize(directory=directory, verbose=verbose)

	def folderize(self, directory=None, verbose=False):
		'''
		1. Place all single files in folders of the same name.
		'''
		Folderizer(directory=directory, verbose=verbose)

	def format(self, directory=None, verbose=False):
		'''
		2. Pull the names of all folders and decide what the title is, based on movie titles in OMDB.
			a. Rename the movie file and folders (i.e., <movie_title> [<year_of_release>])
		'''
		Formatter(directory=directory, verbose=verbose)

	def get_posters(self, directory=None, verbose=False):
		'''
			b. Download the movie poster and name the file poster.png
		'''
		Poster_Finder(directory=directory, verbose=verbose)

	def cleanup(self, directory=None, extensions=None, verbose=False):
		'''
		3. Remove all non-movie files, based on a list of "bad" extensions (i.e., .nfo, .txt, etc)
		'''
		File_Remover(directory=directory, extensions=extensions, verbose=verbose)


if __name__ == '__main__':
	Folderizer(directory=join(getcwd(), 'data', 'Fake_Directory'), verbose=True)