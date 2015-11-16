import requests
import json
from Helper_Functions import *
import re

class Formatter():
	def __init__(self, directory=None, format_type='Movies', data_files=['titles.json'], verbose=True):
		if verbose:
			print '[CURRENT ACTION: FORMATTING MOVIE TITLES]\n'
		# If we haven't already created a titles index file, create one:
		if not exists(join(directory, 'titles.json')): 
			self.initialize_file(directory=directory, filename='titles.json')
		else: # However, if it does exist, 
			#Let's keep track of the files we've already indexed, so we don't duplicate our work:
			with open(join(directory, 'titles.json')) as infile:
				self.indexed_titles = json.load(infile)		
		self.format(directory=directory, data_files=data_files, verbose=verbose)

	def initialize_file(self, directory=None, filename=None):
		'''
		Initialize a JSON file to contain an index of all our new filenames.
		'''
		self.indexed_titles = {'Titles': [], 'Total': 0}
		with open(join(directory, filename), mode='w') as infile:
			json.dump(self.indexed_titles, infile)


	def append_data(self, directory=None, filename='titles.json', new_title=None, imdb_id=None, poster_url=None):
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
			new_entry = {
				'title': new_title,
				'imdb_id': imdb_id,
				'poster': poster_url
			}
			titles_index['Titles'].append(new_entry)
			titles_index['Total'] += 1
			# Write that updated list to the existing file:
			json.dump(titles_index, outfile)

	def search_title(self, url='http://www.omdbapi.com/', search_terms='', release_year='', verbose=False):
		'''
		Searches OMDB api for a movie title closest to the given string.
		'''
		payload = {
			't': search_terms,
			'plot': 'Full',
			'r': 'json',
			'y': release_year #if release_year != '' else ''
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
				return self.search_title(search_terms=search_terms, release_year=release_year) # And recursively try again				

	def search_id(self, url='http://www.omdbapi.com/', imdb_id='', verbose=False):
		'''
		Searches OMDB api for a movie with the given IMdb ID.
		'''
		payload = {
			'i': imdb_id,
			'plot': 'Full',
			'r': 'json'
		}
		req = requests.get(url=url, params=payload)
		if req.status_code == 200:
			response = json.loads(req.content)
			if response['Response'] == "True": # If the response was successful (if we found a movie matching that IMdb ID)
				if verbose:
					print '[SUCCESSFUL]'
					print json.dumps(response, indent=4), '\n'
				return response # Return the full response
			else: # Otherwise, return the failed code -1
				if verbose:
					print '[FAILED] bad IMdb ID.'
				return -1

	def strip_bad_chars(self, title=None):
		'''
		Strips the given title of any characters that aren't allowed in folder/file names.
		'''		
		return re.sub(r'[(<>:"/\\|?*)]', '', title)
	
	def find_release_year(self, title=None, verbose=False):
		'''
		Returns the best candidate for the release year for the given title by removing the improbable candidates.
		'''		
		year_list = re.findall(r"\d{4}", title) # Find all possible "release year" candidates

		if len(year_list) > 0: # If we found any results:
			if verbose:
				print 'Release Year Candidates: {year_list}'.format(year_list=year_list)
			removal_list = []
			for year in year_list:
				if int(year) < 1900: # We won't be dealing with movies before the 1900's
					removal_list.append(str(year))
			for remove_string in removal_list: # For each string that matches the removal process,
				year_list.remove(remove_string) # Remove that string		

			# Add only the last one as that is the most likely candidate of a real candidate (this won't be true when resolutions are at 4K)		
			release_year = year_list[-1] # This will also be the only candidate if there is only one candidate

			if verbose:
				print 'Best Guess for Release Year: {release_year}'.format(release_year=release_year)
			return release_year
		else:
			return ''

	def format(self, directory=None, data_files=[], verbose=False):
		'''
		Formats every folder/filename in the given directory according to the movie title closest to the folder/filename.
		'''				
		for title in listdir(directory):
			if str(title) not in data_files and title not in [entry['title'] for entry in self.indexed_titles['Titles']]: # Let's not process the titles.json file or duplicate our work
				new_title = " ".join(map(str.title, re.findall(r"\w+|\w+'\w+|\w+-\w+|\w+|[(#$!)]+|'\w+", title)))				
				release_year = self.find_release_year(title=title)
				if "_" in new_title:
					new_title = new_title.replace("_", " ")
				try:
					results = self.search_title(search_terms=new_title, release_year=release_year, verbose=verbose)
				except Exception as error:
					print "[ERROR]", error
					print '[FAILED] search terms: {search_terms}'.format(search_terms=title)
				final_title = results['Title'] + ' [' + results['Year'] + ']'
				final_title = self.strip_bad_chars(title=final_title) # Remove non-viable folder characters
				if verbose:				
					print 'Old Title: {title}'.format(title=title)
					print 'New Title: {new_title}'.format(new_title=new_title)
					print 'Final Title: {final_title}'.format(final_title=final_title)								
					print 'Release Year: {release_year}'.format(release_year=release_year)
					print '[RENAMING {old_title} to {new_title}]\n'.format(old_title=join(directory, title), new_title=join(directory, final_title))				
		 		self.append_data(directory=directory, new_title=final_title, poster_url=results['Poster'], imdb_id=results['imdbID']) # Add the current formatted title to our "titles.json" index file
		 		try:
					rename(join(directory, title), join(directory, final_title)) # Renames the folder
				except Exception as error:
					print error


if __name__ == '__main__':
	from datetime import datetime
	start = datetime.now()
	directory = join(getcwd(), 'data', 'Fake_Directory')
	#directory = 'J:\Films'
	f = Formatter(directory=directory, verbose=True)
	finish = datetime.now() - start
	print "Finished in {total_time} seconds".format(total_time=finish)
