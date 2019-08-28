from unittest import mock, TestCase
from unittest.mock import patch

import faker
import json
import os
import shutil

import movie_file_fixer

module_under_test = "movie_file_fixer"

fake = faker.Faker()

TEST_FOLDER = os.path.join("src", "tests")
TEST_INPUT_FOLDER = os.path.join(TEST_FOLDER, "test_input")
DATA_FILES = ["contents.json", "errors.json"]

TEST_TITLES = {
    "vanilla": os.path.join(TEST_FOLDER, "test_examples", "test_titles.json"),
    "chocolate": os.path.join(TEST_FOLDER, "test_examples", "test_trouble_titles.json"),
}


def create_test_environment(
    test_folder=TEST_INPUT_FOLDER,
    file_extensions=["avi", "mov", "mp4", "txt", "dat", "nfo", "jpg", "png", "mkv"],
    use_extensions=False,
):
    """

    :param str os.path test_folder: The directory where the test environment will be set up.
    :param list file_extensions: A list of file extensions to create individual files, for testing file support.
    :param bool use_extensions:
    :return: test_folder and the example titles used to create the test environment.
    """
    example_titles = []

    if not os.path.exists(TEST_INPUT_FOLDER):
        os.mkdir(TEST_INPUT_FOLDER)

    # Create a bunch of random fake files:
    with open(TEST_TITLES["vanilla"], "r") as infile:
        title_examples = json.load(infile)

    for title_example in title_examples:
        # TODO: Figure out something to do with this description:
        # description = title_example.get('description')
        examples = title_example.get("examples")

        for example in examples:
            filename = os.path.join(test_folder, example)
            if use_extensions:
                for extension in file_extensions:
                    new_filename = filename + "." + extension
                    open(new_filename, "a").close()
            else:
                open(filename, "a").close()

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
            f"{module_under_test}.MovieFileFixer.get_posters",
            directory=TEST_INPUT_FOLDER,
        )
        self.mock_get_posters = self.mock_get_posters_patch.start()

        self.mock_get_subtitles_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.get_subtitles",
            directory=TEST_INPUT_FOLDER,
        )
        self.mock_get_subtitles = self.mock_get_subtitles_patch.start()

    def tearDown(self):
        self.mock_folderize_patch.stop()
        self.mock_cleanup_patch.stop()
        self.mock_format_patch.stop()
        self.mock_get_posters_patch.stop()
        self.mock_get_subtitles_patch.stop()

    def test_folderize_is_called(self):
        """Ensure the folderize() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_folderize.assert_called_once()

    def test_cleanup_is_called(self):
        """Ensure the cleanup() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_cleanup.assert_called_once()

    def test_format_is_called(self):
        """Ensure the format() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_format.assert_called_once()

    def test_get_posters_is_called(self):
        """Ensure the get_posters() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_get_posters.assert_called_once()

    def test_get_subtitles_is_called(self):
        """Ensure the get_subtitles() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=TEST_INPUT_FOLDER)
        self.mock_get_subtitles.assert_called_once()


class FolderizerTestCase(TestCase):
    def setUp(self):
        self.test_folder, self.example_titles = create_test_environment(
            file_extensions=["file"], use_extensions=True
        )
        self.folderizer = movie_file_fixer.Folderizer(directory=TEST_INPUT_FOLDER)
        self.single_files = self.folderizer._find_single_files()

    def tearDown(self):
        shutil.rmtree(self.test_folder)

    def test_find_single_files(self):
        """Ensure all single files that were created were found."""
        for single_file in self.single_files:
            if single_file not in DATA_FILES:
                filename, extension = os.path.splitext(single_file)
                self.assertIn(filename, self.example_titles)

    def test_move_files_into_folders(self):
        """Ensure that all single files that were created moved to folders of the same name."""
        self.folderizer._move_files_into_folders(file_names=self.single_files)
        for single_file in self.single_files:
            filename, extension = os.path.splitext(single_file)
            folder_name = os.path.join(TEST_INPUT_FOLDER, filename)
            new_filename = os.path.join(folder_name, single_file)

            # Ensure it's no longer a file:
            self.assertFalse(os.path.isfile(folder_name))
            # But it still exists (as a folder):
            self.assertTrue(os.path.exists(folder_name))
            # And also as a file inside that folder:
            self.assertTrue(os.path.isfile(new_filename))

    @patch(f"{module_under_test}.Folderizer._find_single_files")
    @patch(f"{module_under_test}.Folderizer._move_files_into_folders")
    def test_folderize(self, _find_single_files, _move_files_into_folders):
        """Ensure all internal methods got called when the folderize() method was called."""
        self.folderizer.folderize()
        _find_single_files.assert_called_once()
        _move_files_into_folders.assert_called_once()

    def test_unfolderize(self):
        """Ensure all files inside a given directory get unfolderized."""
        fake_folder_name = fake.word()
        fake_filename = fake.word()
        fake_file_extension = "." + fake.word()
        self.folderizer.folderize()
        # Set up the test area inside each folder by creating an arbitrary file
        # with an arbitrary file extension inside an arbitrary folder:
        for root, dirs, files in os.walk(TEST_INPUT_FOLDER):
            # print(f'root: {root}, dirs: {dirs}, files: {files}')
            new_folder_name = os.path.join(root, fake_folder_name)
            # print("new_folder_name:", new_folder_name)
            os.mkdir(new_folder_name)
            new_filename = os.path.join(
                new_folder_name, fake_filename + fake_file_extension
            )
            open(new_filename, "a").close()

            # Test that the setup worked and created the file in the correct place:
            should_not_exist = os.path.join(root, fake_filename + fake_file_extension)
            self.assertFalse(os.path.isfile(should_not_exist))
            self.assertTrue(os.path.exists(new_folder_name))
            self.assertTrue(os.path.isfile(new_filename))

        self.folderizer.unfolderize(folder_name=fake_folder_name)

        for root, dirs, files in os.walk(TEST_INPUT_FOLDER):
            new_folder_name = os.path.join(root, fake_folder_name)
            new_filename = os.path.join(
                new_folder_name, fake_filename + fake_file_extension
            )

            # Test that unfolderize pulled the files out of the folder and deleted the folder:
            should_exist_now = os.path.join(root, fake_filename + fake_file_extension)
            self.assertTrue(os.path.isfile(should_exist_now))
            self.assertFalse(os.path.exists(new_folder_name))
            self.assertFalse(os.path.isfile(new_filename))
