# -*- coding: utf-8 -*-
'''
Name: poster_finder.py
Author: Blair Gemmer
Version: 20160618

Description: Reads the "titles.json" file and downloads the poster for each title.
'''

import json
import os

import requests


class PosterFinder:
    def __init__(self, directory=None, contents_file='contents.json', verbose=False):
        if verbose:
            print('[CURRENT ACTION: LOCATING MOVIE POSTERS]\n')
        self.get_posters(directory=directory, contents_file=contents_file, verbose=verbose)

    def perform_request(self, url=None, cookies=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
        }

        print('Downloading {url}'.format(url=url))
        return requests.get(url=url, headers=headers, cookies=cookies)

    def get_posters(self, directory=None, contents_file=None, api_key='967174e1', verbose=None):
        full_path = os.path.join(directory, contents_file)
        if verbose:
            print('[PROCESSING FILE: {full_path}]'.format(full_path=full_path))
        if os.path.exists(full_path):
            # Open file for reading:
            with open(full_path, mode='r', encoding='UTF-8') as infile:
                # Load existing data into titles index list:
                titles_index = json.load(infile)
            for title in titles_index['Titles']:
                title_path = os.path.join(directory, title['title'])
                if os.path.exists(title_path):
                    new_path = os.path.join(directory, title['title'], 'poster.jpg')
                    if verbose:
                        print('[PROCESSING TITLE: {title}]'.format(title=str(title['title'])))
                    poster_url = title['poster']
                    # imdb_id = title['imdb_id']

                    # if imdb_id not in ['', None, ' ', 'N/A']:
                    if poster_url not in ['', None, ' ', 'N/A']:
                        #     poster_url = 'http://img.omdbapi.com/?i={imdb_id}&h=600&apikey={api_key}'.format(imdb_id=imdb_id, api_key=api_key)
                        if verbose:
                            print('[ADDING POSTER URL: {poster_url}]\n'.format(poster_url=poster_url))
                        # urllib.urlretrieve(poster_url, new_path)
                        response = self.perform_request(url=poster_url)

                        if response.status_code == 200:
                            print('[DOWNLOAD COMPLETE]')
                            print('[WRITING FILE] -> {filepath}...\n'.format(filepath=new_path))
                            with open(new_path, 'wb') as outfile:
                                outfile.write(response.content)


if __name__ == '__main__':
    directory = os.path.join('test', 'data', 'Fake_Directory')
    directory = 'J:\\to_sort'
    directory = os.path.join('input')
    PosterFinder(directory=directory, contents_file='contents.json')
