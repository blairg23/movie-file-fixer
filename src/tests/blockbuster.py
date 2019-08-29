"""

Blockbuster creates a movie file library test environment.
"""

import json
import os

TEST_FOLDER = os.path.join("src", "tests")
TEST_INPUT_FOLDER = os.path.join(TEST_FOLDER, "test_input")
DATA_FILES = ["contents.json", "errors.json"]

TEST_TITLES = {
    "pg-13": os.path.join(TEST_FOLDER, "test_examples", "test_titles.json"),
    "r-rated": os.path.join(TEST_FOLDER, "test_examples", "test_trouble_titles.json"),
}


class BlockBusterBuilder:
    """

    :param str os.path test_folder: The directory where the test environment will be set up.
    :param list file_extensions: A list of file extensions to create individual files, for testing file support.
    :param bool use_extensions: Whether to use file extensions to create the files.
    :return: test_folder and the example titles used to create the test environment.

    BlockBusterBuilder (or B-Cubed as she likes to be known on the streets) is a test environment construction class.
    She will build a directory full of movie files or a directory where those movie files have been folderized.
    Her primary purpose is to build a test environment to run unit tests and integration tests on files with titles
    that have been considered "tricky" or "gotchas", such as weird punctuation, single letter titles, and titles that
    contain -or consist wholly of- a year.
    """

    def __init__(
        self,
        level="pg-13",
        test_folder=TEST_INPUT_FOLDER,
        file_extensions=["avi", "mov", "mp4", "txt", "dat", "nfo", "jpg", "png", "mkv"],
        use_extensions=False,
    ):
        self._level = level
        self._test_folder = test_folder
        self._file_extensions = file_extensions
        self._use_extensions = use_extensions

    def _create(self, file_extensions, folderized=False, use_extensions=None):
        """

        :param list file_extensions: A list of file extensions to create individual files, for testing file support.
        :param bool folderized: Whether to folderize the files or keep them unfoldered.
        :param bool use_extensions: Whether to use file extensions to create the files.
        :return: The environment test_folder and the example titles used to create the test environment.

        Creates an environment to perform testing on.
        """
        if file_extensions is None:
            file_extensions = self._file_extensions

        if use_extensions is None:
            use_extensions = self._use_extensions

        example_titles = []

        if not os.path.exists(TEST_INPUT_FOLDER):
            os.mkdir(TEST_INPUT_FOLDER)

        # Create a bunch of random fake files:
        with open(TEST_TITLES[self._level], "r") as infile:
            title_examples = json.load(infile)

        for title_example in title_examples:
            # TODO: Figure out something to do with this description:
            # description = title_example.get('description')
            examples = title_example.get("examples")

            for example in examples:
                # Create a folder with the example title if folderized is True:
                filename = (
                    os.path.join(self._test_folder, example, example)
                    if folderized
                    else os.path.join(self._test_folder, example)
                )
                if use_extensions:
                    for extension in file_extensions:
                        new_filename = filename + "." + extension
                        open(new_filename, "a").close()
                else:
                    open(filename, "a").close()

                example_titles.append(example)

        return self._test_folder, example_titles

    def create_single_file_environment(
        self, file_extensions=None, use_extensions=False
    ):
        """

        :param list file_extensions: A list of file extensions to create individual files, for testing file support.
        :param bool use_extensions: Whether to use file extensions to create the files.
        :return: The environment test_folder and the example titles used to create the test environment.

        Creates a test environment full of individual unfoldered files.
        """
        return self._create(
            file_extensions=file_extensions,
            folderized=False,
            use_extensions=use_extensions,
        )

    def create_folderized_environment(self, file_extensions=None, use_extensions=False):
        """

        :param list file_extensions: A list of file extensions to create individual files, for testing file support.
        :param bool use_extensions: Whether to use file extensions to create the files.
        :return: The environment test_folder and the example titles used to create the test environment.

        Creates a test environment full of folderized files.
        """
        return self._create(
            file_extensions=file_extensions,
            folderized=True,
            use_extensions=use_extensions,
        )
