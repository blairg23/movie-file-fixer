# -*- coding: utf-8 -*-
'''
Name: subtitle_finder.py
Author: Blair Gemmer
Version: 20180313

Description: Reads the "titles.json" file and downloads the subtitle for each title, given a language of preference.
'''

import hashlib
import json
import os

import requests


class SubtitleFinder():
    def __init__(self, directory=None, contents_file='contents.json', language='en', verbose=False):
        if verbose:
            print('[CURRENT ACTION: LOCATING MOVIE SUBTITLES]\n')
        self.get_subtitles(directory=directory, contents_file=contents_file, language=language, verbose=verbose)

    def is_movie_file(self, filename):
        movie_file_extensions = ['.avi', '.mp4', '.mkv', '.mov']
        filename, extension = os.path.splitext(filename)
        if extension in movie_file_extensions:
            return True
        else:
            return False

    def get_hash(self, filepath):
        '''
        This hash function receives the name of the file and returns the hash code.
        '''
        readsize = 64 * 1024
        with open(filepath, 'rb') as f:
            size = os.path.getsize(filepath)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)

        return hashlib.md5(data).hexdigest()

    def perform_request(self, url='http://api.thesubdb.com/', payload=None, cookies=None):
        headers = {
            'User-Agent': 'SubDB/1.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11; https://github.com/blairg23/movie-file-fixer'
        }
        response = requests.get(url=url, params=payload, headers=headers, cookies=cookies)
        if response.status_code == 200:
            print('[REQUESTING FROM URL] {url}\n'.format(url=response.url))
            response = response.text
        else:
            print('[ERROR] {url} failed with status code {status_code}\n'.format(url=response.url, status_code=response.status_code))
        return response

    def search_subtitles(self, hashcode=None):
        payload = {
            'action': 'search',
            'hash': hashcode
        }
        response = self.perform_request(payload=payload)

        return response

    def download_subtitles(self, language='en', hashcode=None):
        payload = {
            'action': 'download',
            'hash': hashcode,
            'language': language
        }
        response = self.perform_request(payload=payload)

        return response

    def get_subtitles(self, directory=None, contents_file=None, language='en', verbose=None):
        full_path = os.path.join(directory, contents_file)
        if verbose:
            print('[PROCESSING FILE: {full_path}]\n'.format(full_path=full_path))
        if os.path.exists(full_path):
            # Open file for reading:
            with open(full_path, mode='r', encoding='UTF-8') as infile:
                # Load existing data into titles index list:
                titles_index = json.load(infile)

            for title in titles_index['Titles']:
                # title_path = "\\\\?\\" + os.path.join(directory, title['title'])
                title_path = os.path.join(directory, title['title'])
                if os.path.exists(title_path):
                    # new_path = "\\\\?\\" + os.path.join(directory, title['title'], '{language}_subtitles.srt'.format(language=language))
                    file_path = None
                    for filename in os.listdir(title_path):
                        if self.is_movie_file(filename=filename):
                            file_path = os.path.join(title_path, filename)

                    if file_path is not None:
                        print('[PROCESSING TITLE: {title}]\n'.format(title=str(title['title'])))

                        try:
                            hashcode = self.get_hash(filepath=file_path)
                        except Exception as e:
                            print('[ERROR] File is Corrupt or Missing.')
                            print(e)
                            print('\n')

                        subtitle_path = os.path.join(directory, title['title'], '{language}_subtitles.srt'.format(language=language))
                        if not os.path.exists(subtitle_path):
                            subtitles_available = self.search_subtitles(hashcode=hashcode)

                            if subtitles_available not in ['', None, ' '] and language in subtitles_available:
                                if verbose:
                                    print('[ADDING SUBTITLE FILE: {language}_subtitles.srt]\n'.format(language=language))

                                try:
                                    subtitles = self.download_subtitles(language=language, hashcode=hashcode)
                                    print('[DOWNLOAD COMPLETE]\n')
                                    print('[WRITING FILE] -> {filepath}...\n'.format(filepath=subtitle_path))
                                    with open(subtitle_path, 'w+', encoding='UTF-8') as outfile:
                                        outfile.writelines(subtitles)
                                except Exception as e:
                                    print(e)
                            else:
                                print('[ERROR] No Subtitles Available for that language ({language}).\n'.format(language=language))
                        else:
                            print('Subtitle already exists. Skipping...')
                    else:
                        print('[ERROR] No movie file exists.\n')

                    print('------------------------------------------------')
            print('[COMPLETE]')


if __name__ == '__main__':
    # directory = os.path.join('test', 'data', 'Fake_Directory')  
    # directory = "C:/Users/Neophile/Desktop/sandboxes/python/movie-file-fixer/input/"
    directory = os.path.join(os.getcwd(), 'input')
    directory = "H:\Films"
    SubtitleFinder(directory=directory, contents_file='contents.json')

    # hashcode = pf.get_hash(filename="C:/Users/Neophile/Desktop/sandboxes/python/movie-file-fixer/input/Flatliners [2017]/FLatliners [2017].mp4")
    # print(hashcode)
    # print(pf.search_subtitles(hashcode=hashcode))
