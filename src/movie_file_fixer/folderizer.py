# -*- coding: utf-8 -*-
"""
Name: folderizer.py
Author: Blair Gemmer
Version: 20160618

Description: Searches a directory and puts all singleton files into
a directory of their namesake.
"""

import os
import shutil


class Folderizer:
    def __init__(
        self, directory=None, data_files=["contents.json", "errors.json"], verbose=False
    ):
        if verbose:
            print("[CURRENT ACTION: MOVING SINGLETON FILES TO FOLDERS]\n")
        self.directory = directory
        self.verbose = verbose
        self.action_counter = 0
        # If the directory has been provided:
        if self.directory is not None:
            self.folderize(directory=self.directory, data_files=data_files)

    def find_single_files(self, directory=None):
        """
        Finds all the files without a folder within a given directory.
        """
        # And find all the single files:
        if self.verbose:
            print(
                "\n[{counter}] Finding files in {path}.".format(
                    counter=self.action_counter, path=directory
                )
            )
        single_files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(os.getcwd(), directory, f))
        ]

        self.action_counter += 1
        return single_files

    def move_files_into_folders(self, file_names=[], data_files=None, directory=None):
        """
        Moves a group of files into their respective folders,
        given a list of file_names.
        Will create the folder if it does not already exist.
        """
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
                if self.verbose:
                    print(
                        '[{action_counter}] [Created Folder] "{folder_name}" [successfully]'.format(
                            action_counter=self.action_counter, folder_name=file_name
                        )
                    )
                self.action_counter += 1

            shutil.move(old_file_path, new_file_path)
            if self.verbose:
                print(
                    '[{action_counter}] [Moved File] "{file_name}" to [Folder] "{folder_name}" [successfully]'.format(
                        action_counter=self.action_counter,
                        file_name=fName,
                        folder_name=file_name,
                    )
                )
            self.action_counter += 1

    def folderize(self, directory=None, data_files=None):
        """
        Puts all singleton files from a directory into a folder of its namesake.
        """
        file_names = self.find_single_files(
            directory=directory
        )  # Get all file_names in the given directory
        self.move_files_into_folders(
            file_names=file_names, data_files=data_files, directory=directory
        )  # And move those into folders, based on the same names

    def unfolderize_all(self, directory):
        """
        Removes all files from every folder and places them into the main directory,
        then removes all the folders.
        """
        # TODO
        pass

    def unfolderize(self, directory, folder_name=None):
        """
        Removes all files from every folder named <folder_name> and places them into the
        current root directory, then removes the folder named <folder_name>.
        """
        for root, dirs, files in os.walk(directory):
            for folder in dirs:
                if folder.lower() == folder_name.lower():
                    for file in self.find_single_files(
                        directory=os.path.join(root, folder)
                    ):
                        old_file_path = os.path.join(root, folder, file)
                        new_file_path = os.path.join(root, file)
                        shutil.move(old_file_path, new_file_path)
                    shutil.rmtree(os.path.join(root, folder))


if __name__ == "__main__":
    directory = os.path.join("test", "data", "Fake_Directory")
    directory = "J:\\Films"
    Folderizer(directory=directory, verbose=False)
