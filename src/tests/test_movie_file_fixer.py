from unittest import mock, TestCase
from unittest.mock import patch

import faker
import json
import os
import shutil

import movie_file_fixer

module_under_test = "movie_file_fixer"

fake = faker.Faker()

TEST_FOLDER = os.path.join('src', 'tests')
TEST_INPUT_FOLDER = os.path.join(TEST_FOLDER, 'test_input')

TEST_TITLES = {
    'vanilla': os.path.join(TEST_FOLDER, 'test_examples', 'test_titles.json'),
    'chocolate': os.path.join(TEST_FOLDER, 'test_examples', 'test_trouble_titles.json')
}


class MovieFileFixerTestCase(TestCase):
    def setUp(self):
        # # Create a bunch of random fake files:
        # with open(TEST_TITLES['vanilla'], 'r') as infile:
        #     title_examples = json.load(infile)
        #
        # path_to_create = os.path.join(TEST_FOLDER, 'test_input')
        #
        # for title_example in self.title_examples:
        #     description = title_example.get('description')
        #     examples = title_example.get('examples')
        #     for example in examples:
        #         filename = os.path.join(path_to_create, example)
        #         open(filename, 'a').close()

        # self.mock_folderize_patch = mock.patch(
        #     f"{module_under_test}.MovieFileFixer.folderize", autospec=True
        # )
        # self.mock_folderize = self.mock_folderize_patch.start()

        # self.mock_MovieFileFixer_patch = mock.patch(
        #     f"{module_under_test}.MovieFileFixer", autospec=True
        # )
        # self.mock_MovieFileFixer = self.mock_MovieFileFixer_patch.start()
        pass

    def tearDown(self):
        # self.mock_folderize_patch.stop()
        # self.mock_MovieFileFixer_patch.stop()
        # shutil.rmtree(self.)
        pass

    @patch(f'{module_under_test}.MovieFileFixer.folderize')
    def test_folderize(self, folderize):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        folderize.assert_called_once()

    @patch(f'{module_under_test}.MovieFileFixer.cleanup')
    def test_cleanup(self, cleanup):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        cleanup.assert_called_once()

    @patch(f'{module_under_test}.MovieFileFixer.format')
    def test_format(self, format):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        format.assert_called_once()

    @patch(f'{module_under_test}.MovieFileFixer.format')
    def test_get_posters(self, get_posters):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        get_posters.assert_called_once()

    @patch(f'{module_under_test}.MovieFileFixer.folderize')
    def test_get_subtitles(self, get_subtitles):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        get_subtitles.assert_called_once()
