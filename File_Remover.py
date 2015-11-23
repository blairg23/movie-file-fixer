# -*- coding: utf-8 -*-
'''
Name: File_Remover.py
Author: Blair Gemmer
Version: 20151122

Description: Removes any files with unwanted extensions like ".txt" or ".dat".
'''

import requests
import json
from Helper_Functions import *

class File_Remover():
	def __init__(self, directory=None, extensions=None, verbose=True):
		if verbose:
			print '[CURRENT ACTION: REMOVING UNWANTED FILES]\n'
		self.remove_files(directory=directory, extensions=extensions, verbose=verbose)

	def remove_files(self, directory=None, extensions=None, verbose=False):
		for root, dirs, files in walk(directory):
			for current_file in files:
				if verbose:
					print '[PROCESSING FILE: {filename}]'.format(filename=current_file)
				if any(current_file.lower().endswith(ext) for ext in extensions):
					remove(join(root, current_file))
					if verbose:
						print '[RESULT: REMOVED]\n'
				else:
					if verbose:
						print '[RESULT: NOT REMOVED]\n'
				# This is not as fast:
				# filename, ext = splitext(current_file)
				# if ext in extensions:
				# 	os.remove(join(root, current_file))

if __name__ == '__main__':
	bad_extensions=['.nfo', '.dat', '.jpg', '.png', '.txt']
	directory = join('data', 'Fake_Directory')
	File_Remover(directory=directory, extensions=bad_extensions)