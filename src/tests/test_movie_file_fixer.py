import os
import shutil
from unittest import mock, TestCase
from unittest.mock import patch

import faker

import movie_file_fixer
import src.tests.blockbuster as blockbuster
import utils

module_under_test = "movie_file_fixer"

fake = faker.Faker()


class MovieFileFixerTestCase(TestCase):
    """
    Checks that upon instantiation with a valid directory string, all methods are being called.
    """

    def setUp(self):
        self.mock_folderize_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.folderize", directory=blockbuster.TEST_INPUT_FOLDER
        )
        self.mock_folderize = self.mock_folderize_patch.start()

        self.mock_cleanup_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.cleanup", directory=blockbuster.TEST_INPUT_FOLDER
        )
        self.mock_cleanup = self.mock_cleanup_patch.start()

        self.mock_format_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.format", directory=blockbuster.TEST_INPUT_FOLDER
        )
        self.mock_format = self.mock_format_patch.start()

        self.mock_get_posters_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.get_posters",
            directory=blockbuster.TEST_INPUT_FOLDER,
        )
        self.mock_get_posters = self.mock_get_posters_patch.start()

        self.mock_get_subtitles_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.get_subtitles",
            directory=blockbuster.TEST_INPUT_FOLDER,
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
        movie_file_fixer.MovieFileFixer(directory=blockbuster.TEST_INPUT_FOLDER)
        self.mock_folderize.assert_called_once()

    def test_cleanup_is_called(self):
        """Ensure the cleanup() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=blockbuster.TEST_INPUT_FOLDER)
        self.mock_cleanup.assert_called_once()

    def test_format_is_called(self):
        """Ensure the format() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=blockbuster.TEST_INPUT_FOLDER)
        self.mock_format.assert_called_once()

    def test_get_posters_is_called(self):
        """Ensure the get_posters() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=blockbuster.TEST_INPUT_FOLDER)
        self.mock_get_posters.assert_called_once()

    def test_get_subtitles_is_called(self):
        """Ensure the get_subtitles() function is being called when a valid instance of MovieFileFixer is instantiated."""
        movie_file_fixer.MovieFileFixer(directory=blockbuster.TEST_INPUT_FOLDER)
        self.mock_get_subtitles.assert_called_once()


class FolderizerTestCase(TestCase):
    def setUp(self):
        test_environment = blockbuster.BlockBusterBuilder(
            level="pg-13",
            test_folder=blockbuster.TEST_INPUT_FOLDER,
            file_extensions=["file"],
            use_extensions=True,
        )
        self.test_folder, self.example_titles = (
            test_environment.create_single_file_environment()
        )
        self.folderizer = movie_file_fixer.Folderizer(directory=blockbuster.TEST_INPUT_FOLDER, verbose=True)
        self.single_files = self.folderizer._find_single_files()

    def tearDown(self):
        # shutil.rmtree(self.test_folder)
        pass

    # def test_find_single_files(self):
    #     """Ensure all single files that were created were found."""
    #     for single_file in self.single_files:
    #         if single_file not in blockbuster.DATA_FILES:
    #             filename, extension = os.path.splitext(single_file)
    #             filename_is_in_list = utils.is_in_list(element=filename, the_list=self.example_titles)
    #             self.assertTrue(filename_is_in_list)

    def test_move_files_into_folders(self):
        """Ensure that all single files that were created moved to folders of the same name."""
        self.folderizer._move_files_into_folders(file_names=self.single_files)
        # for single_file in self.single_files:
        #     print('SINGLE_FILE:', single_file)
        #     filename, extension = os.path.splitext(single_file)
        #     print('FILENAME:', filename)
        #     folder_name = os.path.join(blockbuster.TEST_INPUT_FOLDER, filename)
        #     new_filename = os.path.join(folder_name, single_file)
        #     print('IS FILE:', os.path.isfile(folder_name))
        #     print('IS A FOLDER TOO:', os.path.exists(folder_name))
        #     print('AND THERE IS A FILE INSIDE THE FOLDER:', os.path.isfile(new_filename))
        #
        #     # Ensure it's no longer a file:
        #     self.assertFalse(os.path.isfile(folder_name))
        #     # But it still exists (as a folder):
        #     self.assertTrue(os.path.exists(folder_name))
        #     # And also as a file inside that folder:
        #     self.assertTrue(os.path.isfile(new_filename))

    # @patch(f"{module_under_test}.Folderizer._find_single_files")
    # @patch(f"{module_under_test}.Folderizer._move_files_into_folders")
    # def test_folderize(self, _find_single_files, _move_files_into_folders):
    #     """Ensure all internal methods got called when the folderize() method was called."""
    #     self.folderizer.folderize()
    #     _find_single_files.assert_called_once()
    #     _move_files_into_folders.assert_called_once()
    #
    # def test_unfolderize(self):
    #     """Ensure all files inside a given directory get unfolderized."""
    #     fake_folder_name = fake.word()
    #     fake_filename = fake.word()
    #     fake_file_extension = "." + fake.word()
    #     self.folderizer.folderize()
    #     # Set up the test area inside each folder by creating an arbitrary file
    #     # with an arbitrary file extension inside an arbitrary folder:
    #     for root, dirs, files in os.walk(blockbuster.TEST_INPUT_FOLDER):
    #         new_folder_name = os.path.join(root, fake_folder_name)
    #         os.mkdir(new_folder_name)
    #         new_filename = os.path.join(
    #             new_folder_name, fake_filename + fake_file_extension
    #         )
    #         open(new_filename, "a").close()
    #
    #         # Test that the setup worked and created the file in the correct place:
    #         should_not_exist = os.path.join(root, fake_filename + fake_file_extension)
    #         # It is not a single file name in the movie folder:
    #         self.assertFalse(os.path.isfile(should_not_exist))
    #         # It is a folder name however:
    #         self.assertTrue(os.path.exists(new_folder_name))
    #         # and also a file name inside that folder:
    #         self.assertTrue(os.path.isfile(new_filename))
    #
    #     self.folderizer.unfolderize(folder_name=fake_folder_name)
    #
    #     for root, dirs, files in os.walk(blockbuster.TEST_INPUT_FOLDER):
    #         new_folder_name = os.path.join(root, fake_folder_name)
    #         new_filename = os.path.join(
    #             new_folder_name, fake_filename + fake_file_extension
    #         )
    #
    #         # Test that unfolderize pulled the files out of the folder and deleted the folder:
    #         should_exist_now = os.path.join(root, fake_filename + fake_file_extension)
    #         # Now it is a single file name in the movie folder (unfolderized):
    #         self.assertTrue(os.path.isfile(should_exist_now))
    #         # and no longer a folder name (folder is deleted):
    #         self.assertFalse(os.path.exists(new_folder_name))
    #         # nor is it a single file inside that folder:
    #         self.assertFalse(os.path.isfile(new_filename))
