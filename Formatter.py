import requests
import json
from Helper_Functions import *
import re

class Formatter():
	def __init__(self, directory=None, format_type='Movies', verbose=True):
		if verbose:
			print '[CURRENT ACTION: FORMATTING MOVIE TITLES]\n'
		self.populate_dictionaries()
		# If we haven't already created a titles index file, create one:
		if not exists(join(directory, 'titles.json')): 
			self.initialize_file(directory=directory, filename='titles.json')
		else: # However, if it does exist, 
			#Let's keep track of the files we've already indexed, so we don't duplicate our work:
			with open(join(directory, 'titles.json')) as infile:
				self.indexed_titles = json.load(infile)		
		self.format(directory=directory, verbose=verbose)

	def initialize_file(self, directory=None, filename=None):
		'''
		Initialize a JSON file to contain an index of all our new filenames.
		'''
		self.indexed_titles = {'Titles': [], 'Total': 0}
		with open(join(directory, filename), mode='w') as infile:
			json.dump(self.indexed_titles, infile)


	def append_data(self, directory=None, filename='titles.json', new_title=None):
		'''
		Append new data to an existing JSON file.
		'''
		# Open file for reading:
		with open(join(directory, filename), mode='r') as infile:
			# Load existing data into titles index list:
			titles_index = json.load(infile)
		# Open file for writing:
		with open(join(directory, filename), mode='w') as outfile:    
			# Append the new data to the titles index list:
			titles_index['Titles'].append(new_title)
			titles_index['Total'] += 1
			# Write that updated list to the existing file:
			json.dump(titles_index, outfile)

	def populate_dictionaries(self):
		'''
		Populates a set of dictionaries to be used to 
		'''
		# Populate our commonword dictionary wordlist:
		with open('dictionaries/dictionary.txt', 'r+') as infile:
			self.wordlist = [line.rstrip().lower() for line in infile]	

		# Populate our propername dictionary wordlist:
		with open('dictionaries/proper_names.txt', 'r+') as infile:
			self.proper_names = [line.rstrip().lower() for line in infile]

		# Populate our connectives dictionary wordlist:
		with open('dictionaries/connectives.txt', 'r+') as infile:
			self.connectives = [line.rstrip().lower() for line in infile]

	def search(self, url='http://www.omdbapi.com/', search_terms='', verbose=False):
		'''
		Searches OMDB api for a movie title closest to the given string.
		'''
		payload = {
			't': search_terms,
			'r': 'json'
		}
		req = requests.get(url=url, params=payload)
		if req.status_code == 200:
			response = json.loads(req.content)
			if response['Response'] == "True": # If the response was successful (if we found a movie title)
				if verbose:
					print '[SUCCESSFUL]'
					print json.dumps(response, indent=4), '\n'
				return response # Return the full response
			else: # Otherwise, remove the last word from the title (in case it's a junk word or a year of release),
				search_terms = ' '.join(search_terms.split(' ')[:-1])
				if verbose:
					print '[FAILED] new search terms: {search_terms}'.format(search_terms=search_terms)
				return self.search(search_terms=search_terms) # And recursively try again				


	def format(self, directory=None, verbose=False):
		'''
		Formats every folder/filename in the given directory according to the movie title closest to the folder/filename.
		'''		
		for title in listdir(directory):
			if str(title) != 'titles.json' and title not in self.indexed_titles['Titles']: # Let's not process the titles.json file or duplicate our work
				new_title = " ".join(map(str.title, re.findall(r"\w+'\w+|\w+-\w+|\w+", title)))
				if "_" in new_title:
					new_title = new_title.replace("_", " ")
				try:
					results = self.search(search_terms=new_title, verbose=verbose)
				except Exception as e:
					print "[ERROR]", e
					print '[FAILED] search terms: {search_terms}'.format(search_terms=title)
				final_title = results['Title'] + ' [' + results['Year'] + ']'
				final_title = final_title.replace(':', '') # Remove non-viable folder characters
				if verbose:				
					print 'Old Title: {title}'.format(title=title)
					print 'New Title: {new_title}'.format(new_title=new_title)
					print 'Final Title: {final_title}\n'.format(final_title=final_title)								
					print 'renaming {old_title} to {new_title}'.format(old_title=join(directory, title), new_title=join(directory, final_title))				
				self.append_data(directory=directory, new_title=final_title) # Add the current formatted title to our "titles.json" index file
				rename(join(directory, title), join(directory, final_title)) # Renames the folder


if __name__ == '__main__':
	from datetime import datetime
	start = datetime.now()
	directory = join(getcwd(), 'data', 'Fake_Directory')
	#directory = 'J:\Films'
	f = Formatter(directory=directory, verbose=False)
	finish = datetime.now() - start
	print "Finished in {total_time} seconds".format(total_time=finish)
