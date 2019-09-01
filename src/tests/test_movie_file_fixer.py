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
            f"{module_under_test}.MovieFileFixer.folderize",
            directory=blockbuster.TEST_INPUT_FOLDER,
        )
        self.mock_folderize = self.mock_folderize_patch.start()

        self.mock_cleanup_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.cleanup",
            directory=blockbuster.TEST_INPUT_FOLDER,
        )
        self.mock_cleanup = self.mock_cleanup_patch.start()

        self.mock_format_patch = mock.patch(
            f"{module_under_test}.MovieFileFixer.format",
            directory=blockbuster.TEST_INPUT_FOLDER,
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
        # To suppress the stdout by having verbose=True on Folderizer instantiation:
        self.mock_print_patch = mock.patch("builtins.print")
        self.mock_print = self.mock_print_patch.start()

        test_environment = blockbuster.BlockBusterBuilder(
            level="pg-13",
            test_folder=blockbuster.TEST_INPUT_FOLDER,
            file_extensions=["file"],
            use_extensions=True,
        )
        self.test_folder, self.example_titles = (
            test_environment.create_single_file_environment()
        )
        self.folderizer = movie_file_fixer.Folderizer(
            directory=blockbuster.TEST_INPUT_FOLDER, verbose=True
        )
        self.single_files = self.folderizer._find_single_files()

    def tearDown(self):
        shutil.rmtree(self.test_folder)
        self.mock_print_patch.stop()

    def test_find_single_files(self):
        """Ensure all single files that were created were found."""
        for single_file in self.single_files:
            if single_file not in blockbuster.METADATA_FILENAMES:
                filename, extension = os.path.splitext(single_file)
                filename_is_in_list = utils.is_in_list(
                    element=filename, the_list=self.example_titles
                )
                self.assertTrue(filename_is_in_list)

    def test_move_files_into_folders(self):
        """Ensure that all single files that were created moved to folders of the same name."""
        self.folderizer._move_files_into_folders(filenames=self.single_files)
        for single_file in self.single_files:
            filename, extension = os.path.splitext(single_file)
            folder_name = os.path.join(blockbuster.TEST_INPUT_FOLDER, filename)
            new_filename = os.path.join(folder_name, single_file)

            # Ensure it's no longer a file:
            self.assertFalse(os.path.isfile(folder_name))
            # But it still exists (as a folder):
            self.assertTrue(os.path.exists(folder_name))
            # And also as a file inside that folder:
            self.assertTrue(os.path.isfile(new_filename))

    @patch(f"{module_under_test}.Folderizer._find_single_files")
    @patch(f"{module_under_test}.Folderizer._move_files_into_folders")
    def test_folderize(self, find_single_files_method, move_files_into_folders_method):
        """Ensure all internal methods got called when the folderize() method was called."""
        self.folderizer.folderize()
        find_single_files_method.assert_called_once()
        move_files_into_folders_method.assert_called_once()

    def test_unfolderize(self):
        """Ensure all files inside a given directory get unfolderized."""
        fake_folder_name = fake.word()
        fake_filename = fake.word()
        fake_file_extension = "." + fake.word()
        self.folderizer.folderize()
        # Set up the test area inside each folder by creating an arbitrary file
        # with an arbitrary file extension inside an arbitrary folder:
        for root, dirs, files in os.walk(blockbuster.TEST_INPUT_FOLDER):
            new_folder_name = os.path.join(root, fake_folder_name)
            os.mkdir(new_folder_name)
            new_filename = os.path.join(
                new_folder_name, fake_filename + fake_file_extension
            )
            open(new_filename, "a").close()

            # Test that the setup worked and created the file in the correct place:
            should_not_exist = os.path.join(root, fake_filename + fake_file_extension)
            # It is not a single file name in the movie folder:
            self.assertFalse(os.path.isfile(should_not_exist))
            # It is a folder name however:
            self.assertTrue(os.path.exists(new_folder_name))
            # and also a file name inside that folder:
            self.assertTrue(os.path.isfile(new_filename))

        self.folderizer.unfolderize(folder_name=fake_folder_name)

        for root, dirs, files in os.walk(blockbuster.TEST_INPUT_FOLDER):
            new_folder_name = os.path.join(root, fake_folder_name)
            new_filename = os.path.join(
                new_folder_name, fake_filename + fake_file_extension
            )

            # Test that unfolderize pulled the files out of the folder and deleted the folder:
            should_exist_now = os.path.join(root, fake_filename + fake_file_extension)
            # Now it is a single file name in the movie folder (unfolderized):
            self.assertTrue(os.path.isfile(should_exist_now))
            # and no longer a folder name (folder is deleted):
            self.assertFalse(os.path.exists(new_folder_name))
            # nor is it a single file inside that folder:
            self.assertFalse(os.path.isfile(new_filename))

    def test_unfolderize_all(self):
        """This test does nothing until we've implemented that method."""
        fake_result = self.folderizer.unfolderize_all()
        self.assertEqual(fake_result, None)


class FileRemoverTestCase(TestCase):
    def setUp(self):
        # To suppress the stdout by having verbose=True on FileRemover instantiation:
        self.mock_print_patch = mock.patch("builtins.print")
        self.mock_print = self.mock_print_patch.start()

        self.good_file_extensions = [".avi", ".mov", ".mp4", ".mkv", ".srt"]
        self.bad_file_extensions = [
            ".txt",
            ".dat",
            ".nfo",
            ".bmp",
            ".gif",
            ".jpg",
            ".png",
            ".exe",
        ]
        test_environment = blockbuster.BlockBusterBuilder(
            level="pg-13",
            test_folder=blockbuster.TEST_INPUT_FOLDER,
            file_extensions=self.good_file_extensions + self.bad_file_extensions,
            use_extensions=True,
        )
        self.test_folder, self.example_titles = (
            test_environment.create_single_file_environment()
        )
        self.file_remover = movie_file_fixer.FileRemover(
            directory=blockbuster.TEST_INPUT_FOLDER,
            file_extensions=self.bad_file_extensions,
            verbose=True,
        )

    def tearDown(self):
        shutil.rmtree(self.test_folder)
        self.mock_print_patch.stop()

    def test_remove_files(self):
        """Ensure all files with `bad_extensions` are removed."""
        self.file_remover.remove_files()
        for root, dirs, files in os.walk(self.test_folder):
            for file in files:
                filename, extension = os.path.splitext(file)
                self.assertIn(extension, self.good_file_extensions)
                self.assertNotIn(extension, self.bad_file_extensions)


class FormatterTestCase(TestCase):
    def setUp(self):
        # To suppress the stdout by having verbose=True on Formatter instantiation:
        self.mock_print_patch = mock.patch("builtins.print")
        self.mock_print = self.mock_print_patch.start()

        test_environment = blockbuster.BlockBusterBuilder(
            level="pg-13",
            test_folder=blockbuster.TEST_INPUT_FOLDER,
            use_extensions=False,
        )
        self.test_folder, self.example_titles = (
            test_environment.create_single_file_environment()
        )
        self.formatter = movie_file_fixer.Formatter(
            directory=blockbuster.TEST_INPUT_FOLDER, verbose=True
        )

    def tearDown(self):
        shutil.rmtree(self.test_folder)
        self.mock_print_patch.stop()

    @patch(f"{module_under_test}.Formatter._get_release_year")
    @patch(f"{module_under_test}.Formatter._search")
    def test_search_by_search_terms(self, get_release_year_method, search_method):
        """Ensure searching by some search terms calls the `_get_release_year()` and `_search()` methods."""
        call_counter = 0
        for example_title in self.example_titles:
            for original_filename, metadata in example_title.items():
                search_terms = original_filename
                self.formatter.search_by_search_terms(search_terms=search_terms)
                call_counter += 1
        self.assertEqual(get_release_year_method.call_count, call_counter)
        self.assertEqual(search_method.call_count, call_counter)

    @patch(f"{module_under_test}.Formatter._search")
    def test_search_by_imdb_id(self, search_method):
        """Ensure searching by an IMDb ID calls the `_get_release_year()` and `_search()` methods."""
        call_counter = 0
        for example_title in self.example_titles:
            for original_filename, metadata in example_title.items():
                imdb_id = metadata["imdb_id"]
                self.formatter.search_by_imdb_id(imdb_id=imdb_id)
                call_counter += 1
        self.assertEqual(search_method.call_count, call_counter)

    @patch(f"{module_under_test}.Formatter._get_release_year")
    @patch(f"{module_under_test}.Formatter._search")
    def test_search_by_title(self, get_release_year_method, search_method):
        """Ensure searching by a title calls the `_get_release_year()` and `_search()` methods."""
        call_counter = 0
        for example_title in self.example_titles:
            for original_filename, metadata in example_title.items():
                title = metadata["title"]
                self.formatter.search_by_title(title=title)
                call_counter += 1
        self.assertEqual(get_release_year_method.call_count, call_counter)
        self.assertEqual(search_method.call_count, call_counter)

    def test_format(self):
        """Ensure formatting happens as expected."""
        pass
