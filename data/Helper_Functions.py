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

# Path-specific functions
from os.path import isfile, isdir, join # For comparing file_names
from os.path import abspath # For referencing absolute path
from os.path import exists # Check existence of files or folders
from os.path import join # Join root directory to folder
from os.path import split # Split a path by directory and file.
from os.path import splitext # For splitting the file_name and extension

# Shell utilities
from shutil import move # For moving a file
from shutil import copy2 # For copying a file

# For testing purposes
from sys import exit 

# Regex
import re

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