import unittest
import os
import shutil
from data.CreateDummyData import CreateDummyData



class TestCreateDummyDataMethods(unittest.TestCase):

	def setUp(self):
		current_path, filename= os.path.split(os.path.abspath(__file__)) # To start us in the correct directory
		self.fake_directory_path = os.path.join(current_path, 'data', 'Fake_Directory')

	# def test_remove_fake_directory(self):		
	# 	try:
	# 		shutil.rmtree(self.fake_directory_path)
	# 	except OSError as error:
	# 		print error
	# 	self.assertFalse(os.path.exists(self.fake_directory_path))

	def test_create_fake_directory(self):		
		CDD = CreateDummyData(verbose=False)
		CDD.run(directory=self.fake_directory_path)
		self.assertTrue(os.path.exists(self.fake_directory_path))


if __name__ == '__main__':
	unittest.main()