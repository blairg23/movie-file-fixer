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
DATA_FILES = ['contents.json', 'errors.json']

TEST_TITLES = {
    'vanilla': os.path.join(TEST_FOLDER, 'test_examples', 'test_titles.json'),
    'chocolate': os.path.join(TEST_FOLDER, 'test_examples', 'test_trouble_titles.json')
}


def create_test_environment(test_folder=TEST_INPUT_FOLDER):
    """
    :param os.path test_folder: The directory where the test environment will be set up.
    :return: test_folder and the example titles used to create the test environment.
    """
    example_titles = []

    if not os.path.exists(TEST_INPUT_FOLDER):
        os.mkdir(TEST_INPUT_FOLDER)

    # Create a bunch of random fake files:
    with open(TEST_TITLES['vanilla'], 'r') as infile:
        title_examples = json.load(infile)

    for title_example in title_examples:
        # TODO: Figure out something to do with this description:
        # description = title_example.get('description')
        examples = title_example.get('examples')

        for example in examples:
            filename = os.path.join(test_folder, example)
            open(filename, 'a').close()

            example_titles.append(example)

    return test_folder, example_titles


class MovieFileFixerTestCase(TestCase):
    """
    Checks that upon instantiation with a valid directory string, all methods are being called.
    """
    def setUp(self):
        if not os.path.exists(TEST_INPUT_FOLDER):
            os.mkdir(TEST_INPUT_FOLDER)

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


class FolderizerTestCase(TestCase):
    def setUp(self):
        self.test_folder, self.example_titles = create_test_environment()

        self.folderizer = movie_file_fixer.Folderizer(directory=TEST_INPUT_FOLDER)

        # self.mock_folderize_patch = mock.patch(
        #     f"{module_under_test}.MovieFileFixer.folderize", autospec=True
        # )
        # self.mock_folderize = self.mock_folderize_patch.start()

        # self.mock_MovieFileFixer_patch = mock.patch(
        #     f"{module_under_test}.MovieFileFixer", autospec=True
        # )
        # self.mock_MovieFileFixer = self.mock_MovieFileFixer_patch.start()

    def tearDown(self):
        # self.mock_folderize_patch.stop()
        # self.mock_MovieFileFixer_patch.stop()
        shutil.rmtree(self.test_folder)

    def test_find_single_files(self):
        single_files = self.folderizer.find_single_files()
        for single_file in single_files:
            if single_file not in DATA_FILES:
                self.assertIn(single_file, self.example_titles)
