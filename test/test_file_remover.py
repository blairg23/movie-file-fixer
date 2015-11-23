import unittest
import os
import json
from ..File_Remover import File_Remover

class TestFileRemoverMethods(unittest.TestCase):

	def setUp(self):
		current_path, filename= os.path.split(os.path.abspath(__file__)) # To start us in the correct directory
		self.fake_directory_path = os.path.join(current_path, 'data', 'Fake_Directory')	
		self.extensions = ['.nfo', '.dat', '.jpg', '.png', '.txt']			
		self.file_remover = File_Remover(directory=self.fake_directory_path, extensions=self.extensions, verbose=False)

		# Creates some test files:
		for ext in self.extensions:			
			directory = os.path.join(self.fake_directory_path, 'test_path')
			if not os.path.exists(directory):
				os.makedirs(directory)
			with open(os.path.join(directory, 'test_file'+ext), 'w+') as infile:
				pass

	def test_remove_files(self):
		truth_value = True

		self.file_remover.remove_files(directory=self.fake_directory_path, extensions=self.extensions, verbose=False)

		for root, dirs, files in os.walk(self.fake_directory_path):
			for current_file in files:
				if any(current_file.lower().endswith(ext) for ext in self.extensions):
					truth_value = False
		self.assertTrue(truth_value)

if __name__ == '__main__':
	unittest.main()