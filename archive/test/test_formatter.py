# -*- coding: utf-8 -*-
'''
Name: test_formatter.py
Author: Blair Gemmer
Version: 20151123

Description: Unit Testing for Formatter module
'''

import json
import os
import unittest

from data.CreateDummyData import CreateDummyData

from src.movie_file_fixer.formatter import Formatter


class TestFormatterMethods(unittest.TestCase):

    def setUp(self):
        current_path, filename = os.path.split(os.path.abspath(__file__))  # To start us in the correct directory
        self.fake_directory_path = os.path.join(current_path, 'data', 'Fake_Directory')

        # If the fake test directory hasn't been created yet, create it:
        if not os.path.exists(self.fake_directory_path):
            CDD = CreateDummyData(directory=self.fake_directory_path)
            CDD.run(directory=self.fake_directory_path)

        self.test_file_name = 'test_file.json'
        self.data_files = ['titles.json', self.test_file_name]
        self.test_file_path = os.path.join(self.fake_directory_path, self.test_file_name)
        self.formatter = Formatter(directory=self.fake_directory_path, data_files=self.data_files, verbose=False)
        self.formatter.initialize_file(directory=self.fake_directory_path, filename=self.test_file_name)

    def test_initialize_file(self):
        self.assertTrue(os.path.exists(self.test_file_path))

    def test_append_data(self):
        test_title = 'test_title'
        test_poster_url = 'test.url'
        test_imdb_id = '1234'
        self.formatter.append_data(directory=self.fake_directory_path, filename=self.test_file_name, new_title=test_title, poster_url=test_poster_url, imdb_id=test_imdb_id)
        with open(self.test_file_path) as infile:
            test_dict = json.load(infile)
        truth_data = []
        truth_data.append(test_title == test_dict['Titles'][0]['title'])
        truth_data.append(test_poster_url == test_dict['Titles'][0]['poster'])
        truth_data.append(test_imdb_id == test_dict['Titles'][0]['imdb_id'])
        self.assertTrue(all(truth_data))

    def test_search_title_no_year(self):
        test_title = 'The Matrix'
        test_result = self.formatter.search_title(search_terms=test_title)
        self.assertTrue(test_title in test_result['Title'])

    def test_search_title_with_year(self):
        test_title = 'The Matrix'
        test_result = self.formatter.search_title(search_terms=test_title, release_year='1999')
        self.assertTrue(test_title in test_result['Title'])

    def test_search_id(self):
        test_id = 'tt0133093'
        test_result = self.formatter.search_id(imdb_id=test_id, verbose=False)
        self.assertTrue('The Matrix' in test_result['Title'])

    def test_strip_bad_chars(self):
        test_title_start = 'a<b>c:d"e/f\\g|h?i*'
        test_title_end = self.formatter.strip_bad_chars(title=test_title_start)
        self.assertTrue(test_title_end == 'abcdefghi')

    def test_find_release_year(self):
        test_titles = ['Red Dawn {2012} DVDRIP. Jaybob', '2012 (2009) DVDRip XviD-MAXSPEED']
        years = []
        for title in test_titles:
            years.append(self.formatter.find_release_year(title=title))
        truth_data = []
        truth_data.append('2012' in years[0])  # if the year 2012 is in the title Red Dawn (2012)
        truth_data.append('2009' in years[1])  # if the year 2009 is in the title 2012 (2009)
        self.assertTrue(all(truth_data))  # If both of the above were true, this will be true

    def test_format(self):
        # Read in a list of the test titles, properly formatted:
        current_path, filename = os.path.split(os.path.abspath(__file__))  # To start us in the correct directory
        path = os.path.join(current_path, 'data', 'good_titles.txt')
        with open(path, mode='r') as infile:
            good_titles = infile.read().splitlines()
        # Run format (This step has already been completed):
        self.formatter.format(directory=self.fake_directory_path, data_files=self.data_files)
        list_of_folders = os.listdir(self.fake_directory_path)  # Check the directory listing
        for filename in self.data_files:
            list_of_folders.remove(filename)  # Remove 'test_file.json' and 'titles.json'
        # Should return True if all the titles have been renamed (make sure to check capitalization when debugging this function):
        self.assertTrue(all([filename in good_titles for filename in list_of_folders]))


if __name__ == '__main__':
    unittest.main()
