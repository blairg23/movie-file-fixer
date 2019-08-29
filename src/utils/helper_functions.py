# -*- coding: utf-8 -*-
"""

Description: Create one file to import all functions that are repeatedly imported or written during this project.
"""

import errno
import os


def listdir_fullpath(d):
    """ Returns the full path of every file or folder within a given directory, d """
    return [os.path.join(d, f) for f in os.listdir(d)]


def is_in_list(element, the_list):
    """
    Prints boolean value of whether the element is in the list.

    * element can be a singleton value or a list of values.
    * the_list can be a single list or a list of lists.
    """
    return any([element in the_list]) or any([element in row for row in the_list])


def is_in_folder(folder_path=None, file_name=None):
    """
    Returns a boolean value whether the file or folder is located in the given folder path.

    folder_path is a string value representing the full (or relative) path of the directory to search in.
    file_name is a string value representing the file or folder name to search for.
    """
    import os.path
    if os.path.exists(folder_path):
        print(file_name in os.listdir(folder_path))
    print(os.listdir(folder_path))


def find_single_files(directory):
    """
    Finds all the files without a folder within a given directory
    """
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def find_folders(directory):
    """
    Finds all the folders in a given directory
    """
    return [os.path.join(directory, o) for o in os.listdir(directory) if os.path.isdir(os.path.join(directory, o))]


def get_folder_name(folder_path):
    """
    Returns the folder name, given a full folder path
    """
    return folder_path.split(os.sep)[-1]


def silent_remove(filename):
    """
    Removes a given filename, unless it raises an error.
    Doesn't throw an error if there isn't such a file existent.
    """
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
