# -*- coding: utf-8 -*-
'''
Name: CreateDummyData
Author: Blair Gemmer
Version: 20150608

Description: Creates dummy data for to test results for MovieFilenameFixer.py
'''

from Helper_Functions import *

fileCounter = 0

class CreateDummyData():

	def __init__(self, directory=None, verbose=False):
		self.verbose=verbose

	def createDummyData(self, filePrefix='fake.file', folderName='Fake_Directory', filetypes=['avi'] ,fileNames=['1', '2', '3', '4', '5']):

		def createNewFiles(filePrefix, folderName, filetypes):
			global fileCounter
			'''Creates files to match the given folder name and a list of file types.
			'''
			for fType in filetypes: # For each of the file types:
				# Create a new file name with that file prefix and file type:
				newFileName = '{fPrefix}.{fType}'.format(fPrefix=filePrefix, fType=fType) 
				if exists(newFileName):
					if self.verbose:
						print '[{fileCounter}] [Skipping File] \"{fileName}\" already exists in [Folder] \"{folderName}\"'.format(fileCounter=fileCounter, fileName=newFileName, folderName=folderName)
					fileCounter += 1
				else:
					with open(newFileName, 'a+') as newFile: # And create the new dummy file in that folder
						if self.verbose:
							print '[{fileCounter}] [Writing File] \"{fileName}\" to [Folder] \"{folderName}\"'.format(fileCounter=fileCounter, fileName=newFileName, folderName=folderName)
						fileCounter += 1

		def createInnerFoldersAndFiles(filePrefix, innerFolderNames, filetypes):
			'''Creates the inner folders from the list of folder names
			and the files to match those folder names and a list of 
			file types.
			'''		
			# Create a new file prefix implying we're in an inner folder:
			filePrefix = '{fPrefix}.from.folder'.format(fPrefix=filePrefix)

			for fName in innerFolderNames: # For each of the inner folder names,
				# Create a new file prefix for that folder name:
				fPrefix = '{fPrefix}.{fName}'.format(fPrefix=filePrefix, fName=fName)

				if not exists (fName): # If the folder doesn't exist,
					mkdir(fName) # Create it
					chdir(fName) # Change it to the current working directory
					# and create files based on that folder name and list of file types:
					createNewFiles(filePrefix=fPrefix, folderName=fName, filetypes=filetypes)
				else: # If the folder does exist,
					chdir(fName) # Change it to the current working directory
					# and create files based on the current folder name and list of file types:
					createNewFiles(filePrefix=fPrefix, folderName=fName, filetypes=filetypes)
				chdir('..') # Don't forget to move back up to the original directory!

		
		# Create the new folder:
		if not exists(folderName): # If the folder doesn't exist,	
			mkdir(folderName) # Create it
			chdir(folderName) # and change it to the current working directory		
			# Finally, create those inner folders and files:
			createInnerFoldersAndFiles(filePrefix=filePrefix, innerFolderNames=fileNames, filetypes=filetypes)
		else: # If the folder does exist,
			chdir(folderName) # Change it to the current working directory
			# Finally, create those inner folders and files:
			createInnerFoldersAndFiles(filePrefix=filePrefix, innerFolderNames=fileNames, filetypes=filetypes)

		# Create outer files based on the file names and file types:
		# for fName in fileNames:
		# 	# Create a new file prefix for that file name:
		# 	fPrefix = '{fPrefix}.{fName}'.format(fPrefix=filePrefix, fName=fName)
		# 	createNewFiles(filePrefix=fPrefix, folderName=folderName, filetypes=filetypes)

	def run(self, directory='Fake_Directory'):
		filePrefix='single.file'
		folderName = directory
		filetypes = ['avi', 'mov', 'mp4', 'txt', 'dat', 'nfo', 'jpg', 'png', 'mkv']
		fileNames = [

					# Normal title:
					'The.Bay.2012.LiMiTED.BRRip.XviD.RoSubbed-playXD',										
					'Hansel.&.Gretel.Witch.Hunters.2013.DVDRip.XviD-P2P',

					# For testing folder names with underscores in them
					'Ordinary_Decent_Criminal.DVDRip_devilwarez.pl',

					# For testing titles with hyphens in the name:
					'Kick-Ass (2010) R5 XViD-MAXSPEED',
					'Kick-Ass 2 (2013) [1080p]',
					'Bio-Dome (1996) - DVD Rip - XVID',

					# For testing titles that have numbers in them:
					'22.Jump.Street.2014.1080p.BluRay.x264.anoXmous',
					'30 Days Of Night[2007]',
					'\'71 (2014) [1080p]',
					
					# For testing titles that have purposeful periods in them:
					'Snatch.2000.1080p.BluRay.x264.anoXmous',
					#'Fantastic.Mr.Fox.DVDRip.XviD-MOViERUSH', # Can't fix this yet
					# 'W.[2008]DvDrip-aXXo', # Can't fix this yet

					# For testing titles with colons in them:
					'Avengers Age of Ultron (2015) [1080p]',
					#'Abraham.Lincoln.Vampire.Hunter.2012.DVDRip.XviD-ALLiANCE', # Can't fix this yet
					'Sherlock Holmes A Game of Shadows (2011) DVDRip XviD-MAXSPEED',

					# For testing titles with years (or numbers) as the title:
					'2012 (2009) DVDRip XviD-MAXSPEED',
					'1408[2007]DvDrip[Eng]-aXXo',
					'300[2006]DvDrip[Eng]-aXXo',

					# For testing duplicate names:
					'Red Dawn {2012} DVDRIP. Jaybob',
					'Red.Dawn.1984.720p.BrRip.x264.Obit11.ThumperDC',
					'Poltergeist (1982) [1080p]',
					'Poltergeist 2015 1080p HDRip x264 AC3-JYK',
					'The.Girl.With.The.Dragon.Tattoo-[www.speed.cd ]-[2009]DvDrip-aXXo',
					'The Girl With The Dragon Tattoo (2011) (HD)',
					
					# For testing crazy punctuation in titles:
					'What the #$! Do We (K)now!',
					'Fired Up! (2009)'
					]


		self.createDummyData(filePrefix=filePrefix, folderName=folderName, filetypes=filetypes, fileNames=fileNames)

if __name__ == '__main__':
	CDD = CreateDummyData()
	CDD.run()