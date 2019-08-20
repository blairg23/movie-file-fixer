# -*- coding: utf-8 -*-
'''
Name: test_file_remover.py
Author: Blair Gemmer
Version: 20151123

Description: Unit Testing for File_Remover module
'''

import os
import shutil
import unittest

from ..file_remover import File_Remover


class TestFileRemoverMethods(unittest.TestCase):

    def setUp(self):
        current_path, filename = os.path.split(os.path.abspath(__file__))  # To start us in the correct directory
        self.fake_directory_path = os.path.join(current_path, 'data', 'Fake_Directory')
        self.extensions = ['.nfo', '.dat', '.jpg', '.png', '.txt']
        self.file_remover = File_Remover(directory=self.fake_directory_path, extensions=self.extensions, verbose=False)

        # Creates some test files:
        for ext in self.extensions:
            self.test_directory = os.path.join(self.fake_directory_path, 'test_path')
            if not os.path.exists(self.test_directory):
                os.makedirs(self.test_directory)
            with open(os.path.join(self.test_directory, 'test_file' + ext), 'w+') as infile:
                pass

    def test_remove_files(self):
        truth_value = True

        self.file_remover.remove_files(directory=self.fake_directory_path, extensions=self.extensions, verbose=False)

        for root, dirs, files in os.walk(self.fake_directory_path):
            for current_file in files:
                if any(current_file.lower().endswith(ext) for ext in self.extensions):
                    truth_value = False
        shutil.rmtree(self.test_directory)  # Cleanup
        self.assertTrue(truth_value)


if __name__ == '__main__':
    unittest.main()
