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


def create_test_environment(test_folder=TEST_INPUT_FOLDER, file_extensions=['avi', 'mov', 'mp4', 'txt', 'dat', 'nfo', 'jpg', 'png', 'mkv']):
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
        self.mock_folderize_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.folderize", directory=TEST_INPUT_FOLDER
        )
        self.mock_folderize = self.mock_folderize_patch.start()

        self.mock_cleanup_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.cleanup", directory=TEST_INPUT_FOLDER
        )
        self.mock_cleanup = self.mock_cleanup_patch.start()

        self.mock_format_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.format", directory=TEST_INPUT_FOLDER
        )
        self.mock_format = self.mock_format_patch.start()

        self.mock_get_posters_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.get_posters", directory=TEST_INPUT_FOLDER
        )
        self.mock_get_posters = self.mock_get_posters_patch.start()

        self.mock_get_subtitles_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.get_subtitles", directory=TEST_INPUT_FOLDER
        )
        self.mock_get_subtitles = self.mock_get_subtitles_patch.start()

    def tearDown(self):
        self.mock_folderize_patch.stop()
        self.mock_cleanup_patch.stop()
        self.mock_format_patch.stop()
        self.mock_get_posters_patch.stop()
        self.mock_get_subtitles_patch.stop()

    def test_folderize(self):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_folderize.assert_called_once()

    def test_cleanup(self):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_cleanup.assert_called_once()

    def test_format(self):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_cleanup.assert_called_once()

    def test_get_posters(self):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_get_posters.assert_called_once()

    def test_get_subtitles(self):
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_get_subtitles.assert_called_once()


class FolderizerTestCase(TestCase):
    def setUp(self):
        self.test_folder, self.example_titles = create_test_environment()

        self.folderizer = movie_file_fixer.Folderizer(directory=TEST_INPUT_FOLDER)

    def tearDown(self):
        shutil.rmtree(self.test_folder)

    def test_find_single_files(self):
        single_files = self.folderizer.find_single_files()
        for single_file in single_files:
            if single_file not in DATA_FILES:
                self.assertIn(single_file, self.example_titles)
