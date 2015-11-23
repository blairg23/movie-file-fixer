import unittest
import os
import json
from ..Poster_Finder import Poster_Finder

class TestPosterFinderMethods(unittest.TestCase):

	def setUp(self):
		current_path, filename= os.path.split(os.path.abspath(__file__)) # To start us in the correct directory
		self.fake_directory_path = os.path.join(current_path, 'data', 'Fake_Directory')
		self.test_file_name = 'test_file.json'
		self.test_file_path = os.path.join(self.fake_directory_path, self.test_file_name)		

		# Create a test file:
		self.test_title = 'test_title'
		self.test_imdb_id = 1234
		self.test_poster_url = 'http://globalgamejam.org/sites/default/files/styles/game_sidebar__normal/public/game/featured_image/promo_5.png'

		# Create a test folder:
		self.test_folder_path = os.path.join(self.fake_directory_path, self.test_title)
		if not os.path.exists(self.test_folder_path):
			os.makedirs(self.test_folder_path)

		indexed_titles = {'Titles': [], 'Total': 0}
		with open(self.test_file_path, mode='w') as infile:
			json.dump(indexed_titles, infile)
		# Open file for reading:
		with open(self.test_file_path, mode='r') as infile:
			# Load existing data into titles index list:
			titles_index = json.load(infile)
		# Open file for writing:
		with open(self.test_file_path, mode='w') as outfile:    
			# Append the new data to the titles index list:
			new_entry = {
				'title': self.test_title,
				'imdb_id': self.test_imdb_id,
				'poster': self.test_poster_url
			}
			titles_index['Titles'].append(new_entry)
			titles_index['Total'] += 1
			# Write that updated list to the existing file:
			json.dump(titles_index, outfile)

		# Finally, create our test object:
		self.poster_finder = Poster_Finder(directory=self.fake_directory_path, filename=self.test_file_name, verbose=False)		

	def test_find_poster(self):
		self.poster_finder.get_posters(directory=self.fake_directory_path, filename=self.test_file_name, verbose=False)
		#self.assertTrue(os.path.exists(os.path.join(directory, filename)))

if __name__ == '__main__':
	unittest.main()