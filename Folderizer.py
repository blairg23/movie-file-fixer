# -*- coding: utf-8 -*-
'''
Name: Folderizer
Author: Blair Gemmer
Version: 20150608

Description: Searches a directory and puts all singleton files into
a directory of their namesake.
'''

from Helper_Functions import *

class Folderizer():
	def __init__(self, directory=None, verbose=False):
		self.directory = directory
		self.verbose = verbose
		self.action_counter = 0		
		# If the directory has been provided:
		if self.directory != None:
			self.cwd = directory			
			self.folderize(self.directory)

	def find_single_files(self, directory):
		'''
		Finds all the files without a folder within a given directory.
		'''		
		# And find all the single files:
		if self.verbose:
			print '\n[{counter}] Finding files in {path}.'.format(counter=self.action_counter, path=self.cwd)		
		single_files = [f for f in listdir(directory) if isfile(join(directory,f))]
		self.action_counter += 1
		return single_files


	def move_files_into_folders(self, file_names):
		'''
		Moves a group of files into their respective folders, 
		given a list of file_names.
		Will create the folder if it does not already exist.
		'''
		for fName in file_names:			
			file_name, fileExt = splitext(fName) # Extract the file_name from the extension			
			if not exists(join(self.cwd, file_name)): # If the folder doesn't already exist:
				print join(self.cwd,file_name)
			 	mkdir(join(self.cwd, file_name)) # Then create it
			 	if self.verbose:
			 		print '[{action_counter}] [Created Folder] \"{folder_name}\" [successfully]'.format(action_counter=self.action_counter, folder_name=file_name)
			 	self.action_counter += 1
			old_path = join(self.cwd, fName)			
			new_path = join(self.cwd, file_name, fName)			
			move(old_path, new_path)
			if self.verbose:
				print '[{action_counter}] [Moved File] \"{file_name}\" to [Folder] \"{folder_name}\" [successfully]'.format(action_counter=self.action_counter, file_name=fName, folder_name=file_name)
			self.action_counter += 1

	def folderize(self, directory):		
		'''
		Puts all singleton files from a directory into a folder of its namesake.
		'''		
		file_names = self.find_single_files(directory) # Get all file_names in the given directory					
		self.move_files_into_folders(file_names) # And move those into folders, based on the same names

	def unfolderize(self, directory):
		'''
		Removes all files from every folder and places them into the main directory,
		then removes all the folders.
		'''
		#TODO
		pass

if __name__ == '__main__':
	cwd = join(getcwd(),'data', 'Fake_Directory')
	fs = Folderizer(directory=cwd, verbose=True)