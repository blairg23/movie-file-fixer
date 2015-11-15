import unittest
import os
import shutil
from CreateDummyData import CreateDummyData



class TestCreateDummyDataMethods(unittest.TestCase):
	def test_remove_fake_directory(self):
		fake_directory_path = os.path.join(os.getcwd(), 'data', 'Fake_Directory')
		try:
			shutil.rmtree(fake_directory_path)
		except OSError as error:
			print error
		self.assertFalse(os.path.exists(fake_directory_path))

	def test_create_fake_directory(self):
		fake_directory_path = os.path.join(os.getcwd(), 'data', 'Fake_Directory')
		CDD = CreateDummyData(verbose=False)
		CDD.run(directory=fake_directory_path)
		self.assertTrue(os.path.exists(fake_directory_path))


if __name__ == '__main__':
	unittest.main()