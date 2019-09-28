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

import argparse
import sys

from movie_file_fixer.file_remover import FileRemover
from movie_file_fixer.folderizer import Folderizer
from movie_file_fixer.formatter import Formatter
from movie_file_fixer.poster_finder import PosterFinder
from movie_file_fixer.subtitle_finder import SubtitleFinder


def main():
    args = parse_args(sys.argv[1:])

    movie_file_fixer = MovieFileFixer(
        directory=args.directory,
        file_extensions=args.file_extensions,
        metadata_filename=args.metadata_filename,
        language=args.language,
        result_type=args.result_type,
        verbose=args.verbose,
    )
    movie_file_fixer.folderize()
    movie_file_fixer.cleanup()
    movie_file_fixer.format()
    movie_file_fixer.get_posters()
    movie_file_fixer.get_subtitles()


def parse_args(args):
    """

    :param list args: The list of arguments to parse.
    :return argparse.Namespace: An object which contains all parsed arguments as attributes.

    Convert argument strings to objects and assign them as attributes of the namespace.
    Return the populated namespace.
    """
    parser = argparse.ArgumentParser(
        description="A command line utility to help create a rich multimedia library out of your backup movie collection."
    )
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        help="A directory containing raw movie files and folders.",
    )
    parser.add_argument(
        "--file_extensions",
        "-e",
        action="append",
        default=[],
        help="A directory containing raw movie files and folders.",
    )
    parser.add_argument(
        "--metadata_filename",
        "-f",
        type=str,
        default="metadata.json",
        help="To specify a pre-built or custom metadata filename.",
    )
    parser.add_argument(
        "--language",
        "-l",
        type=str,
        default="en",
        help="To specify a two-character language encoding for subtitles.",
    )
    parser.add_argument(
        "--result_type",
        "-r",
        type=str,
        default="movie",
        choices=['movie', 'series', 'episode'],
        help="To specify a type of IMDb object result to return metadata and poster information for.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Set this flag to enable verbose print statements.",
    )
    return parser.parse_args(args)


class MovieFileFixer:
    def __init__(
        self,
        directory,
        file_extensions=[
            ".idx",
            ".sub",
            ".nfo",
            ".dat",
            ".jpg",
            ".png",
            ".txt",
            ".exe",
        ],
        metadata_filename="metadata.json",
        language="en",
        result_type='movie',
        verbose=False,
    ):
        default_file_extensions = [
            ".idx",
            ".sub",
            ".nfo",
            ".dat",
            ".jpg",
            ".png",
            ".txt",
            ".exe",
        ]
        self._directory = directory
        self._file_extensions = (
            file_extensions if file_extensions else default_file_extensions
        )
        self._metadata_filename = metadata_filename
        self._language = language
        self._result_type = result_type
        self._verbose = verbose

    def folderize(
        self, directory=None, metadata_filename=None, folder_name="subs", verbose=None
    ):
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

        if verbose is None:
            verbose = self._verbose

        folderizer = Folderizer(
            directory=directory, metadata_filename=metadata_filename, verbose=verbose
        )
        folderizer.folderize()
        folderizer.unfolderize(folder_name=folder_name)

    def cleanup(self, directory=None, file_extensions=None, verbose=None):
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

        if verbose is None:
            verbose = self._verbose

        file_remover = FileRemover(
            directory=directory, file_extensions=file_extensions, verbose=verbose
        )
        file_remover.remove_files()

    def format(self, directory=None, result_type=None, verbose=None):
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

        if verbose is None:
            verbose = self._verbose

        if result_type is None:
            result_type = self._result_type

        formatter = Formatter(directory=directory, result_type=result_type, verbose=verbose)
        formatter.format()

    def get_posters(self, directory=None, metadata_filename=None, verbose=None):
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

        if verbose is None:
            verbose = self._verbose

        poster_finder = PosterFinder(
            directory=directory, metadata_filename=metadata_filename, verbose=verbose
        )
        poster_finder.get_posters()

    def get_subtitles(
        self, directory=None, metadata_filename=None, language=None, verbose=None
    ):
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

        if language is None:
            language = self._language

        if verbose is None:
            verbose = self._verbose

        subtitle_finder = SubtitleFinder(
            directory=directory,
            metadata_filename=metadata_filename,
            language=language,
            verbose=verbose,
        )
        subtitle_finder.get_subtitles()


#
# if __name__ == "__main__":
#     fake_directory = os.path.join(os.getcwd(), "test", "data", "Fake_Directory")
#     directory = fake_directory
#     directory = os.path.join(os.getcwd(), "input")
#     directory = os.path.join("H:", "tosort", "input")
#     MovieFileFixer(
#         directory=directory,
#         metadata_filename=["contents.json", "errors.json"],
#         verbose=False,
#     )
