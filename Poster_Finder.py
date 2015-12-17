# -*- coding: utf-8 -*-
'''
Name: Poster_Finder.py
Author: Blair Gemmer
Version: 20151123

Description: Reads the "titles.json" file and downloads the poster for each title.
'''

import requests
import json
from Helper_Functions import *
import urllib

class Poster_Finder():
	def __init__(self, directory=None, filename=None, verbose=False):
		if verbose:
			print '[CURRENT ACTION: LOCATING MOVIE POSTERS]\n'
		self.get_posters(directory=directory, filename=filename, verbose=verbose)

	def get_posters(self, directory=None, filename=None, verbose=None):
		full_path = join(directory, filename)
		if verbose:
			print '[PROCESSING FILE: {full_path}]'.format(full_path=full_path)
		if exists(full_path):
			# Open file for reading:
			with open(full_path, mode='r') as infile:
				# Load existing data into titles index list:
				titles_index = json.load(infile)
			for title in titles_index['Titles']:
				new_path = join(directory, str(title['title']), 'poster.jpg')
				if verbose:
					print '[PROCESSING TITLE: {title}]'.format(title=str(title['title']))												
				poster_url = title['poster']
				if poster_url != 'N/A':
					if verbose:
						print '[ADDING POSTER URL: {poster_url}]\n'.format(poster_url=poster_url)
					urllib.urlretrieve(poster_url, new_path)

if __name__ == '__main__':
	current_path = join(getcwd(), 'test', 'data', 'Fake_Directory')	
	pf = Poster_Finder(directory=current_path, filename='titles.json')