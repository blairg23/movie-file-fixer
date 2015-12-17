# -*- coding: utf-8 -*-
'''
Name: print_titles.py
Author: Blair Gemmer
Version: 20151217

Description: Prints out titles from a given directory's titles.json file
for assisting in debugging functionality.
'''

import os, json, errno, re

def byteify(input):
	'''
	Converts input into raw bytes.
	'''
	if isinstance(input, dict):
		return {byteify(key):byteify(value) for key,value in input.iteritems()}
	elif isinstance(input, list):
		return [byteify(element) for element in input]
	elif isinstance(input, unicode):
		return input.encode('utf-8')
	else:
		return input

def get_directory_filenames(directory=None, verbose=False):
	'''
	Generator to return filenames of a given directory.
	'''
	for filename in os.listdir(directory):
		yield filename

def get_directory_titles(directory=None, titles_filename='titles.json'):
	'''
	Returns the titles from the given JSON file (usually titles.json).
	'''
	if titles_filename in get_directory_filenames(directory=directory):
		titles_filename = os.path.join(directory, titles_filename)
		with open(titles_filename, 'r') as infile:
			titles_file = json.load(infile)
			titles = titles_file['Titles']
		for title in titles:
			yield byteify(title['title'])

def print_directory_titles(directory=None, titles_filename='titles.json'):
	'''
	Writes the titles from the given JSON file (usually titles.json) to
	a file named 'titles.txt'.
	'''

	def silent_remove(filename=None):
		# Remove the file if it already exists:
		try:
			os.remove(filename)
		except OSError as e: # this would be "except OSError, e:" before Python 2.6
			if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
				raise # re-raise exception if a different error occured

	silent_remove(filename='titles.txt')
	with open('titles.txt', 'a+') as outfile:
		for title in get_directory_titles(directory=directory):
			print 'Writing', byteify(title)
			outfile.write(byteify(title) + '\n')

def compare_titles(directory=None, titles_filename='titles.json'):
	'''
	Compares the given directory and titles file (usually titles.json)
	and returns any that don't match.
	'''
	for title in get_directory_titles(directory=directory):		
		new_title = " ".join(map(str.title, re.findall(r"\w+|\w+'\w+|\w+-\w+|\w+|[(#$!)]+|'\w+", title)))				
		print new_title
if __name__=='__main__':
	directory = 'J:\Films'
	titles_filename = 'titles.json'

	#for filename in get_directory_filenames(directory=directory):
	#	print filename
	#print_directory_titles(directory=directory)	
	compare_titles(directory=directory)