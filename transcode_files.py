# -*- coding: utf-8 -*-
'''
Name: transcode_files.py
Author: Blair Gemmer
Version: 20160724

Description: 

Transcodes files in a bad format to a good format.

'''
import os
import subprocess


def add_command_flags(command_string=None, command_flags=None):
    for command_flag, command_value in command_flags.iteritems():
        command_string += command_flag + ' ' + command_value + ' '
    return command_string


file_directory = 'J:\\to_sort'

good_format = '.mp4'
bad_formats = ['.avi', '.mkv', '.mov']

command = 'C:\Program Files\Handbrake\HandBrakeCLI.exe'
encoding = 'x264'
rf_value = '20'
audio_quality = '160'
default_command_flags = {'-e': encoding, '-q': rf_value, '-B': audio_quality}
command_string = command + ' '

if len(default_command_flags.keys()) > 0:
    command_string = add_command_flags(
        command_string=command_string,
        command_flags=default_command_flags
    )

for filename in os.listdir(file_directory):
    full_filepath = '\"' + os.path.join(file_directory, filename) + '\"'
    fName, extension = os.path.splitext(filename)
    if extension in bad_formats:
        output_filename = fName + good_format
        output_filepath = os.path.join(file_directory, output_filename)
        if not os.path.exists(output_filepath):
            full_output_filepath = '\"' + output_filepath + '\"'
            additional_command_flags = {'-i': full_filepath, '-o': full_output_filepath}
            if len(additional_command_flags.keys()) > 0:
                command_string = add_command_flags(
                    command_string=command_string,
                    command_flags=additional_command_flags
                )
            print(command_string)
            subprocess.Popen(command_string)
    else:
        print('Extension {extension} does not match bad formats.'.format(extension=extension))
