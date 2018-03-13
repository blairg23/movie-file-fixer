# -*- coding: utf-8 -*-
'''
Name: file_remover.py
Author: Blair Gemmer
Version: 20160618

Description: os.removes any files with unwanted extensions like ".txt" or ".dat".
'''

import os


class FileRemover:
    def __init__(self, directory=None, extensions=None, verbose=True):
        if verbose:
            print('[CURRENT ACTION: REMOVING UNWANTED FILES]\n')
        self.remove_files(directory=directory, extensions=extensions, verbose=verbose)

    def remove_files(self, directory=None, extensions=None, verbose=False):
        for root, dirs, files in os.walk(directory):
            for current_file in files:
                if verbose:
                    print('[PROCESSING FILE: {filename}]'.format(filename=current_file))
                if any(current_file.lower().endswith(ext) for ext in extensions):
                    os.remove(os.path.join(os.getcwd(), root, current_file))
                    if verbose:
                        print('[RESULT: REMOVED]\n')
                else:
                    if verbose:
                        print('[RESULT: NOT REMOVED]\n')
                # This is not as fast:
                # filename, ext = splitext(current_file)
                # if ext in extensions:
                # 	os.os.remove(os.path.join(root, current_file))


if __name__ == '__main__':
    bad_extensions = ['.nfo', '.dat', '.jpg', '.png', '.txt']
    directory = os.path.join('test', 'data', 'Fake_Directory')
    FileRemover(directory=directory, extensions=bad_extensions, verbose=False)
