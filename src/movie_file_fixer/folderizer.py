# -*- coding: utf-8 -*-
"""
Description: Searches a directory and puts all singleton files into
a directory of their namesake.
"""

import os
import shutil


class Folderizer:
    def __init__(
        self, directory, data_files=["contents.json", "errors.json"], verbose=False
    ):
        if verbose:
            print("[CURRENT ACTION: MOVING SINGLETON FILES TO FOLDERS]\n")
        self._directory = directory
        self._data_files = data_files
        self._verbose = verbose
        self._action_counter = 0

    def _find_single_files(self, directory=None):
        """
        :param str directory: The directory to locate single files.
        :return list: A list of single files.

        Finds all the files without a folder within a given directory.
        """
        if directory is None:
            directory = self._directory

        # And find all the single files:
        if self._verbose:
            print(f"\n[{self._action_counter}] Finding files in {directory}.")
        single_files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(os.getcwd(), directory, f))
        ]

        self._action_counter += 1
        return single_files

    def _move_files_into_folders(self, directory=None, data_files=None, file_names=[]):
        """

        :param str directory: Directory of single files to move into folders.
        :param list data_files: A list of metadata files to ignore when folderizing.
        :param file_names:
        :return: None

        Moves a group of files into their respective folders, given a list of file_names.
        Will create the folder if it does not already exist.
        """
        if directory is None:
            directory = self._directory

        if data_files is None:
            data_files = self._data_files

        valid_file_names = [fName for fName in file_names if fName not in data_files]
        for fName in valid_file_names:
            old_file_path = os.path.join(os.getcwd(), directory, fName)
            file_name, file_ext = os.path.splitext(
                fName
            )  # Extract the file_name from the extension
            new_file_path = os.path.join(os.getcwd(), directory, file_name)
            if not os.path.exists(
                new_file_path
            ):  # If the folder doesn't already exist:
                os.mkdir(new_file_path)  # Then create it
                if self._verbose:
                    print(
                        f'[{self._action_counter}] [Created Folder] "{file_name}" [successfully]'
                    )
                self._action_counter += 1

            shutil.move(old_file_path, new_file_path)
            if self._verbose:
                print(
                    f'[{self._action_counter}] [Moved File] "{fName}" to [Folder] "{file_name}" [successfully]'
                )
            self._action_counter += 1

    def folderize(self, directory=None, data_files=None):
        """

        :param str directory: Directory of single files to folderize.
        :param list data_files: A list of metadata files to ignore when folderizing.
        :return: None

        Puts all singleton files from a directory into a folder of its namesake.
        """
        if directory is None:
            directory = self._directory

        if data_files is None:
            data_files = self._data_files

        file_names = self._find_single_files(
            directory=directory
        )  # Get all file_names in the given directory
        self._move_files_into_folders(
            file_names=file_names, data_files=data_files, directory=directory
        )  # And move those into folders, based on the same names

    def unfolderize_all(self, directory=None):
        """
        Removes all files from every folder and places them into the main directory,
        then removes all the folders.
        """
        if directory is None:
            directory = self._directory

        # TODO
        pass

    def unfolderize(self, directory=None, folder_name=None):
        """

        :param str directory: Directory of folderized files.
        :param str folder_name: Folder name to unfolderize.
        :return: None

        Removes all files from every folder named <folder_name> and places them into the
        current root directory, then removes the folder named <folder_name>.
        """
        if directory is None:
            directory = self._directory

        for root, dirs, files in os.walk(directory):
            for folder in dirs:
                if folder.lower() == folder_name.lower():
                    for file in self._find_single_files(
                        directory=os.path.join(root, folder)
                    ):
                        old_file_path = os.path.join(root, folder, file)
                        new_file_path = os.path.join(root, file)
                        shutil.move(old_file_path, new_file_path)
                    shutil.rmtree(os.path.join(root, folder))
