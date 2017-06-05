# -*- coding: utf-8 -*-
'''
Name: Helper_Functions.py
Author: Blair Gemmer
Version: 20151105

Description: Create one file to import all functions that are repeatedly imported or written during this project.
'''

# OS-specific functions
from os import walk # For cascading through a group of folders to find all files
from os import mkdir # For creating individual folders
from os import listdir # For finding singleton files
from os import pardir # For referencing parent directory (equivalent to ..)
from os import sep as divider # the os specific folder separator
from os import getcwd # Current working directory
from os import chdir # Change the current working directory
from os import remove # Remove the specified file
from os import rename # Renames a given file

# Path-specific functions
from os.path import isfile, isdir, join # For comparing file_names
from os.path import abspath # For referencing absolute path
from os.path import exists # Check existence of files or folders
from os.path import join # Join root directory to folder
from os.path import split # Split a path by directory and file.
from os.path import splitext # For splitting the file_name and extension

# For throwing errors:
import errno

# Shell utilities
from shutil import move # For moving a file
from shutil import copy2 # For copying a file

# For testing purposes
from sys import exit 

# Regex
import re

def listdir_fullpath(d):	
	''' Returns the full path of every file or folder within a given directory, d '''
	import os
	return [os.path.join(d, f) for f in os.listdir(d)]


def is_in_list(element, the_list):
	'''
	Prints boolean value of whether the element is in the list.

	* element can be a singleton value or a list of values.
	* the_list can be a single list or a list of lists.
	'''
	return any([element in the_list]) or any([element in row for row in the_list]) 

def is_in_folder(folder_path=None, file_name=None):
	'''
	Returns a boolean value whether the file or folder is located in the given folder path.

	folder_path is a string value representing the full (or relative) path of the directory to search in.
	file_name is a string value representing the file or folder name to search for.
	'''
	import os.path
	if os.path.exists(folder_path):
		print(file_name in os.listdir(folder_path))
	print(os.listdir(folder_path))
	
def find_single_files(directory):
	'''
	Finds all the files without a folder within a given directory
	'''
	return [f for f in listdir(directory) if isfile(join(directory,f))]	

def find_folders(directory):
	'''
	Finds all the folders in a given directory
	'''
	return [join(directory,o) for o in listdir(directory) if isdir(join(directory,o))]

def get_folder_name(folder):
	'''
	Returns the folder name, given a full folder path
	'''
	return folder.split(os.sep)[-1]

def silent_remove(filename):
	'''
	Removes a given filename, unless it raises an error. 
	Doesn't throw an error if there isn't such a file existent.
	'''
	try:
		remove(filename)
	except OSError as e: # this would be "except OSError, e:" before Python 2.6
		if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
			raise # re-raise exception if a different error occured