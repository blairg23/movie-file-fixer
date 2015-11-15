import unittest
import os
import json
from Formatter import Formatter


class TestFormatterMethods(unittest.TestCase):

	def setUp(self):
		self.fake_directory_path = os.path.join(os.getcwd(),'data', 'Fake_Directory')
		self.test_file_name = 'test_file.json'
		self.test_file_path = os.path.join(self.fake_directory_path, self.test_file_name)
		self.formatter = Formatter(directory=self.fake_directory_path, verbose=False)		

	def test_initialize_file(self):				
		self.formatter.initialize_file(directory=self.fake_directory_path, filename=self.test_file_name)
		self.assertTrue(os.path.exists(self.test_file_path))		

	def test_append_data(self):				
		test_title = 'test_title'
		self.formatter.append_data(directory=self.fake_directory_path, filename=self.test_file_name, new_title=test_title)
		with open(self.test_file_path) as infile:
			test_dict = json.load(infile)		
		self.assertTrue(test_title in test_dict['Titles'])

	def test_search(self):
		test_title = 'The Matrix'
		test_result = self.formatter.search(search_terms=test_title)
		self.assertTrue(test_title in test_result['Title'])

	def test_strip_bad_chars(self):
		test_title_start = 'a<b>c:d"e/f\\g|h?i*'
		test_title_end = self.formatter.strip_bad_chars(title=test_title_start)
		self.assertTrue(test_title_end == 'abcdefghi')

	def test_format(self):
		path = os.path.join('data', 'bad_titles.txt')
		with open(path, mode='r') as infile:
			bad_titles = infile.readlines()
		

if __name__ == '__main__':
	unittest.main()