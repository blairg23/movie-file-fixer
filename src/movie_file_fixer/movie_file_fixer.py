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
        extensions=[".nfo", ".dat", ".jpg", ".png", ".txt", ".exe"],
        data_files=["contents.json", "errors.json"],
        verbose=False,
    ):
        self.folderize(directory=directory, data_files=data_files, verbose=verbose)
        self.cleanup(directory=directory, extensions=extensions, verbose=verbose)
        self.format(directory=directory, verbose=verbose)
        self.get_posters(directory=directory, data_files=data_files, verbose=verbose)
        self.get_subtitles(directory=directory, data_files=data_files, verbose=verbose)

    def folderize(self, directory, data_files, verbose=False):
        """
        1. Place all single files in folders of the same name.
            a. Pull all subtitle files out of folders if they are in them.
        """
        folderizer = Folderizer(
            directory=directory, data_files=data_files, verbose=verbose
        )
        folderizer.folderize()
        folderizer.unfolderize(folder_name="subs")

    def cleanup(self, directory, extensions, verbose=False):
        """
        2. Remove all non-movie files, based on a list of "bad" extensions (i.e., .nfo, .txt, etc)
        """
        FileRemover(directory=directory, extensions=extensions, verbose=verbose)

    def format(self, directory, verbose=False):
        """
        3. Pull the names of all folders and decide what the title is, based on movie titles in OMDb API.
            a. Rename the movie file and folders (i.e., <movie_title> [<year_of_release>])
        """
        Formatter(directory=directory, verbose=verbose)

    def get_posters(self, directory, data_files, verbose=False):
        """
        4. Download the movie poster and name the file poster.<extension>
        (where <extension> is the original extension of the poster file)
        """
        contents_file = data_files[0]
        PosterFinder(directory=directory, contents_file=contents_file, verbose=verbose)

    def get_subtitles(
        self, directory, data_files, language="en", verbose=False
    ):
        """
        5. Download the movie subtitles and name the file <language>_subtitles.srt
        """
        contents_file = data_files[0]
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
    # directory = "C:/Users/Neophile/Desktop/sandboxes/python/movie-file-fixer/input/"
    MovieFileFixer(
        directory=directory, data_files=["contents.json", "errors.json"], verbose=False
    )
