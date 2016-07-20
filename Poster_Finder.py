# -*- coding: utf-8 -*-
'''
Name: Poster_Finder.py
Author: Blair Gemmer
Version: 20160618

Description: Reads the "titles.json" file and downloads the poster for each title.
'''

import requests
import json
import os
import urllib

class Poster_Finder():
	def __init__(self, directory=None, contents_file='contents.json', verbose=False):
		if verbose:
			print '[CURRENT ACTION: LOCATING MOVIE POSTERS]\n'
		self.get_posters(directory=directory, contents_file=contents_file, verbose=verbose)

	def get_posters(self, directory=None, contents_file=None, verbose=None):
		full_path = os.path.join(directory, contents_file)
		if verbose:
			print '[PROCESSING FILE: {full_path}]'.format(full_path=full_path)		
		if os.path.exists(full_path):			
			# Open file for reading:
			with open(full_path, mode='r') as infile:
				# Load existing data into titles index list:
				titles_index = json.load(infile)
			for title in titles_index['Titles']:
				title_path = "\\\\?\\" + os.path.join(directory, title['title'])
				if os.path.exists(title_path):
					new_path = "\\\\?\\" + os.path.join(directory, title['title'], 'poster.jpg')
					if verbose:
						print '[PROCESSING TITLE: {title}]'.format(title=str(title['title']))												
					poster_url = title['poster']
					if poster_url != 'N/A':
						if verbose:
							print '[ADDING POSTER URL: {poster_url}]\n'.format(poster_url=poster_url)
						urllib.urlretrieve(poster_url, new_path)

if __name__ == '__main__':
	directory = os.path.join('test', 'data', 'Fake_Directory')	
	directory = 'J:\\to_sort'
	pf = Poster_Finder(directory=directory, contents_file='contents.json')