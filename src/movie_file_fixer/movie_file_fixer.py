# -*- coding: utf-8 -*-
"""
Description:

Executes a five part movie folder formatting workflow for a given directory.

The workflow actions are as follows:

1. [Folderizer] Searches a directory and puts all singleton files into a directory of their namesake.

2. [FileRemover] Removes any files with unwanted extensions like ".txt" or ".dat".

3. [Formatter] Formats all the files and folders in a given directory based on their movie title
and creates a title directory called "contents.json", which also contains poster information.

4. [PosterFinder] Reads that "contents.json" file and downloads the poster for each title.

5. [SubtitleFinder] Reads the "contents.json" file and downloads the subtitle for each title.

"""

import os

from movie_file_fixer.folderizer import Folderizer
from movie_file_fixer.file_remover import FileRemover
from movie_file_fixer.formatter import Formatter
from movie_file_fixer.poster_finder import PosterFinder
from movie_file_fixer.subtitle_finder import SubtitleFinder


class MovieFileFixer:
    def __init__(
        self,
        directory,
        file_extensions=[".nfo", ".dat", ".jpg", ".png", ".txt", ".exe"],
        metadata_filename='metadata.json',
        verbose=False,
    ):
        self.folderize(
            directory=directory, metadata_filename=metadata_filename, verbose=verbose
        )
        self.cleanup(directory=directory, file_extensions=file_extensions, verbose=verbose)
        self.format(directory=directory, verbose=verbose)
        self.get_posters(
            directory=directory, metadata_filename=metadata_filename, verbose=verbose
        )
        self.get_subtitles(
            directory=directory, metadata_filename=metadata_filename, verbose=verbose
        )

    def folderize(self, directory=None, metadata_filename=None, folder_name="subs", verbose=False):
        """

        :param str directory: The directory of single files to folderize.
        :param str metadata_filename: The metadata file to ignore when folderizing.
        :param str folder_name: Folder to unfolderize files from.
        :param bool verbose: Whether or not to activate verbose mode.
        :return: None

        1. Place all single files in folders of the same name.
            a. Pull all subtitle files out of folders if they are in them.
        """
        if directory is None:
            directory = self._directory

        if metadata_filename is None:
            metadata_filename = self._metadata_filename

        folderizer = Folderizer(
            directory=directory, metadata_filename=metadata_filename, verbose=verbose
        )
        folderizer.folderize()
        folderizer.unfolderize(folder_name=folder_name)

    def cleanup(self, directory=None, file_extensions=None, verbose=False):
        """

        :param str directory: The directory of movie folders to clean.
        :param list file_extensions: A list of file extensions to remove.
        :param bool verbose: Whether or not to activate verbose mode.
        :return: None

        2. Remove all non-movie files, based on a list of "bad" extensions (i.e., .nfo, .txt, etc)
        """
        if directory is None:
            directory = self._directory

        if file_extensions is None:
            file_extensions = self._file_extensions

        file_remover = FileRemover(
            directory=directory, file_extensions=file_extensions, verbose=verbose
        )
        file_remover.remove_files()

    def format(self, directory=None, result_type=None, verbose=False):
        """

        :param str directory: The directory of movie folders to format.
        :param str result_type: What type of IMDb object you want returned. Valid Options: [`movie`, `series`, `episode`]
        :param bool verbose: Whether or not to activate verbose mode.
        :return: None

        3. Pull the names of all folders and decide what the title is, based on movie titles in OMDb API.
            a. Rename the movie file and folders (i.e., <movie_title> [<year_of_release>])
        """
        if directory is None:
            directory = self._directory

        formatter = Formatter(directory=directory, verbose=verbose)
        formatter.format(result_type=result_type)


    def get_posters(self, directory=None, metadata_filename=None, verbose=False):
        """

        :param str directory: The directory of movie folders to get posters for.
        :param str metadata_filename: The metadata file to get the poster URL from.
        :param bool verbose: Whether or not to activate verbose mode.
        :return: None

        4. Download the movie poster and name the file poster.<extension>
        (where <extension> is the original extension of the poster file)
        """
        if directory is None:
            directory = self._directory

        if metadata_filename is None:
            metadata_filename = self._metadata_filename

        poster_finder = PosterFinder(directory=directory, metadata_filename=metadata_filename, verbose=verbose)
        poster_finder.download_posters()

    def get_subtitles(self, directory=None, metadata_filename=None, language="en", verbose=False):
        """

        :param str directory: The directory of movie folders to get subtitles for.
        :param str metadata_filename: The metadata file to get movie paths from.
        :param str language: The two-character language code for the subtitle language to retrieve.
        :param bool verbose: Whether or not to activate verbose mode.
        :return: None

        5. Download the movie subtitles and name the file <language>_subtitles.srt
        """
        if directory is None:
            directory = self._directory

        if metadata_filename is None:
            metadata_filename = self._metadata_filename

        contents_file = metadata_filename[0]
        SubtitleFinder(
            directory=directory,
            contents_file=contents_file,
            language=language,
            verbose=verbose,
        )


if __name__ == "__main__":
    fake_directory = os.path.join(os.getcwd(), "test", "data", "Fake_Directory")
    directory = fake_directory
    directory = os.path.join(os.getcwd(), "input")
    directory = os.path.join("H:", "tosort", "input")
    MovieFileFixer(
        directory=directory,
        metadata_filename=["contents.json", "errors.json"],
        verbose=False,
    )
