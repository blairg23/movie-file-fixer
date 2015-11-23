import unittest
import os
import json
from ..Poster_Finder import Poster_Finder

class TestPosterFinderMethods(unittest.TestCase):

	def setUp(self):
		current_path, filename= os.path.split(os.path.abspath(__file__)) # To start us in the correct directory
		self.fake_directory_path = os.path.join(current_path, 'data', 'Fake_Directory')
		self.test_file_name = 'test_file.json'
		self.data_files = ['titles.json', self.test_file_name]
		self.test_file_path = os.path.join(self.fake_directory_path, self.test_file_name)
		self.formatter = Poster_Finder(directory=self.fake_directory_path, data_files=self.data_files, verbose=False)		

	def test_find_poster(self):
		pass

if __name__ == '__main__':
	unittest.main()