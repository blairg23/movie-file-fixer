# -*- coding: utf-8 -*-
'''
Name: formatter.py
Author: Blair Gemmer
Version: 20170604

Description: Formats all the files and folders in a given directory based on their movie title 
and creates a title directory called "contents.json", which also contains poster information.
'''

import json
import os
import re

import requests


class Formatter:
    def __init__(self, directory=None, format_type='Movies', data_files=['contents.json', 'errors.json'], debug=False, verbose=False):
        self.debug = debug
        if directory != None:
            if verbose:
                print('[CURRENT ACTION: FORMATTING MOVIE TITLES]\n')
            # If we haven't already created a table of contents file, create one:
            if not os.path.exists(os.path.join(directory, 'contents.json')):
                self.indexed_titles = {'Titles': [], 'Metadata': [], 'Total': 0}
                self.initialize_file(directory=directory, filename='contents.json', initial_data=self.indexed_titles)
            else:  # However, if it does exist,
                # Let's keep track of the files we've already indexed, so we don't duplicate our work:
                with open(os.path.join(directory, 'contents.json'), encoding='UTF-8') as infile:
                    self.indexed_titles = json.load(infile)
            if not os.path.exists(os.path.join(directory, 'errors.json')):
                self.error_titles = {'Titles': [], 'Total': 0}
                self.initialize_file(directory=directory, filename='errors.json', initial_data=self.error_titles)
            else:
                with open(os.path.join(directory, 'errors.json'), encoding='UTF-8') as infile:
                    self.error_titles = json.load(infile)
            self.format(directory=directory, data_files=data_files, verbose=verbose)
        else:
            print('[ERROR] Need to specify a directory to work on.')

    def initialize_file(self, directory=None, filename=None, initial_data=None):
        '''
        Initialize a JSON file with some initial data

        i.e., To contain an index of all our new filenames

        or all the files that errored out.
        '''
        with open(os.path.join(directory, filename), mode='w') as outfile:
            json.dump(initial_data, outfile)

    def append_content_data(self, directory=None, filename='contents.json', new_content=None, content_key=None):
        '''

        Append new data to an existing JSON file that represents the contents of the given directory.

        i.e., Movie title information or entire IMDb metadata relating to a particular title.

        '''
        # Open file for reading:
        with open(os.path.join(directory, filename), mode='r') as infile:
            # Load existing data into titles index list:
            contents_file = json.load(infile)
        # Open file for writing:
        with open(os.path.join(directory, filename), mode='w') as outfile:
            # Append the new data to the titles index list:
            contents_file[content_key].append(new_content)
            # Only count the titles:
            if content_key == 'Titles':
                contents_file['Total'] += 1
            # Write that updated list to the existing file:
            json.dump(contents_file, outfile)

    # @Todo: Deprecate this method:
    def search_title(self, url='http://www.omdbapi.com/', apikey='967174e1', title='', release_year='', run_number=0, max_recurse=10, verbose=False):
        '''
        Searches OMDB api for a movie title closest to the given string.
        '''
        headers = {
            'content-type': 'application/json'
        }
        payload = {
            't': title,
            'plot': 'Full',
            'r': 'json',
            'y': release_year,  # if release_year != '' else ''
            'apikey': apikey
        }
        req = requests.get(url=url, params=payload, headers=headers)
        if req.status_code == 200:
            response = req.json()
            if response['Response'] == "True":  # If the response was successful (if we found a movie title)
                if verbose:
                    print('[SUCCESSFUL]')
                    print(json.dumps(response, indent=4), '\n')
                return response  # Return the full response
            else:  # Otherwise, remove the last word from the title (in case it's a junk word or a year of release),
                title = ' '.join(title.split(' ')[:-1])
                if verbose:
                    print('[FAILED] new search terms: {search_terms}\n'.format(title=title))
                if run_number < max_recurse:
                    return self.search_title(title=title, release_year=release_year, run_number=run_number + 1, verbose=verbose)  # And recursively try again
                else:
                    raise Exception('ERROR: Max recursion depth.')

    def search_id(self, url='http://www.omdbapi.com/', apikey='967174e1', imdb_id=None, verbose=False):
        '''
        Searches OMDB api for a movie with the given IMdb ID.
        '''
        headers = {
            'content-type': 'application/json'
        }
        payload = {
            'i': imdb_id,
            'plot': 'Full',
            'r': 'json',
            'apikey': apikey
        }
        req = requests.get(url=url, params=payload, headers=headers)
        if req.status_code == 200:
            response = req.json()
            if response['Response'] == "True":  # If the response was successful (if we found a movie title)
                if verbose:
                    print('[SUCCESSFUL]')
                    print(json.dumps(response, indent=4), '\n')
                return response  # Return the full response
            else:
                verbose = True
                if verbose:
                    print('ERROR: Not a valid IMDb ID.')
                raise Exception('ERROR: Not a valid IMDb ID.')

    def search_movies(self, url='http://www.omdbapi.com/', apikey='967174e1', search_terms='', release_year='', run_number=0, max_recurse=10, verbose=False):
        '''
        Searches OMDB api for a movie title closest to the given string.
        '''
        headers = {
            'content-type': 'application/json'
        }
        payload = {
            's': search_terms,
            'r': 'json',
            'apikey': apikey
        }
        req = requests.get(url=url, params=payload, headers=headers)
        if req.status_code == 200:
            response = req.json()
            if response['Response'] == "True":  # If the response was successful (if we found a movie title)
                if verbose:
                    print('[SUCCESSFUL]')
                    print(json.dumps(response, indent=4), '\n')

                valid_results = []
                # If more than one movie matched the search query:
                print(response['Search'])
                if len(response['Search']) > 0:
                    # Iterate through all the movies
                    for search_result in response['Search']:
                        # If all the words in the title of the current movie are in the search query,
                        # print('search_terms:', search_terms)
                        # print('Title:', search_result['Title'].split(' '))
                        # print(all([self.strip_bad_chars(word).lower() in search_terms.lower() for word in search_result['Title'].split(' ')]) and search_result['Year'] == release_year)
                        if all([self.strip_bad_chars(word).lower() in search_terms.lower() for word in search_result['Title'].split(' ')]) and search_result['Year'] == release_year:
                            # Add it to the list of valid titles
                            valid_results.append(search_result)

                if len(valid_results) == 1:
                    response = self.search_id(imdb_id=valid_results[0]['imdbID'])
                elif len(valid_results) > 1:
                    verbose = True
                    found_it = False
                    if verbose:
                        print('[RESPONSE] The following movies matched this search query:')
                        print(json.dumps(valid_results, indent=4))
                        print('Attempting to find the one that is a movie.')
                        for result in valid_results:
                            if result['Type'] == 'movie':
                                response = self.search_id(imdb_id=valid_results[0]['imdbID'])
                                found_it = True

                        if not found_it:
                            raise Exception('ERROR: More than one title matched this search query, but neither was a movie.')
                else:
                    verbose = True
                    if verbose:
                        print('[ERROR] Not a valid search query.')
                        print('[FAILED] search terms: {search_terms}\n'.format(search_terms=search_terms))
                    raise Exception('[ERROR] Not a valid search query.')
                return response  # Return the full response
            # else:
            #     verbose = True
            #     if verbose:
            #         print('[ERROR] Not a valid search query.')
            #         print('[FAILED] search terms: {search_terms}\n'.format(search_terms=search_terms))
            #     raise Exception('ERROR: Not a valid search query.')
            else:  # Otherwise, remove the last word from the title (in case it's a junk word or a year of release),
                search_terms = ' '.join(search_terms.split(' ')[:-1])
                if verbose:
                    print('[FAILED] new search terms: {search_terms}\n'.format(search_terms=search_terms))
                if run_number < max_recurse:
                    return self.search_movies(search_terms=search_terms, release_year=release_year, run_number=run_number + 1, verbose=verbose)  # And recursively try again
                else:
                    raise Exception('ERROR: Max recursion depth.')

    def search_tv_id(self, url='http://www.omdbapi.com/', apikey='967174e1', imdb_id='', season='1', verbose=False):
        '''
        Searches OMDB api for a television series with the given IMdb ID and the given season.
        '''
        payload = {
            'i': imdb_id,
            'Season': season,
            'apikey': apikey
        }
        req = requests.get(url=url, params=payload)
        if req.status_code == 200:
            response = req.json()
            if response['Response'] == "True":  # If the response was successful (if we found a movie matching that IMdb ID)
                if verbose:
                    print('[SUCCESSFUL]')
                    print(json.dumps(response, indent=4), '\n')
                return response  # Return the full response
            else:  # Otherwise, return the failed code -1
                if verbose:
                    print('[FAILED] bad IMdb ID.')
                return -1

    def find_release_year(self, title=None, verbose=False):
        '''
        Returns the best candidate for the release year for the given title by removing the improbable candidates.
        '''
        year_list = re.findall(r"\d{4}", title)  # Find all possible "release year" candidates
        if len(year_list) > 0:  # If we found any results:
            if verbose:
                print('Release Year Candidates: {year_list}'.format(year_list=year_list))
            removal_list = []
            for year in year_list:
                if int(year) < 1900:  # We won't be dealing with movies before the 1900's
                    # For each string that matches the removal process,
                    year_list.remove(str(year))  # Remove that string

            # Add only the last one as that is the most likely candidate of a real candidate (this won't be true when resolutions are at 4K)
            if len(year_list) > 0:  # Make sure there is still at least one candidate
                release_year = year_list[-1]  # This will also be the only candidate if there is only one candidate

                if verbose:
                    print('Best Guess for Release Year: {release_year}'.format(release_year=release_year))
                return release_year
            else:
                return ''
        else:
            return ''

    def strip_bad_chars(self, title=None):
        '''
        Strips the given title of any characters that aren't allowed in folder/file names.
        '''
        return re.sub(r'[(<>:"/\\|?*)]', '', title)

    def format(self, directory=None, data_files=[], verbose=False, file_type='movie'):
        '''
        Formats every folder/filename in the given directory according to the movie title closest to the folder/filename.
        '''

        def cleanup(title=None):
            '''
            Fixes some problems with titles, like punctuation
            and contractions or possessive cases.

            Also, strips the given title of any characters that aren't allowed in folder/file names.
            '''
            new_title = re.sub(r"[^\$#! | ^\w\d'\s]+", ' ', title).replace('_', ' ')
            new_title = new_title.strip()

            # Not good, but might contain some regex we want later (LEAVE FOR NOW):
            # new_title = join(map(str.title, re.findall(r"\w+|\w+'\w+|\w+-\w+|\w+|[(#$!)]+|'\w+", title)))

            # Not sure if we need this yet:
            # new_title = re.sub(r'[(<>:"/\\|?*)]', '', new_title)
            return new_title

        # s = ''.os.path.join(ch for ch in s if ch not in exclude)
        for title in os.listdir(directory):
            # Let's not process the contents.json file or duplicate our work:           
            if str(title) not in data_files and title not in [entry['title'] if entry != [] else [] for entry in self.indexed_titles['Titles']]:
                new_title = cleanup(title=title)

                # Limit the size of the new title to max words:
                max_size = 9

                if len(new_title.split(' ')) > max_size:
                    new_title = ' '.join(new_title.split(' ')[0:max_size])
                release_year = self.find_release_year(title=title, verbose=False)
                if release_year != '':
                    new_title = new_title.replace(release_year, '').strip()
                # print(new_title, release_year)
                try:
                    try:
                        # results = self.search_title(search_terms=new_title, release_year=release_year, verbose=verbose)
                        results = self.search_movies(search_terms=new_title, release_year=release_year, verbose=verbose)
                    except Exception as e:
                        print(e)
                        new_title = {
                            'original_filename': title,
                            'title': new_title
                        }
                        if title not in [entry['title'] if entry != [] else [] for entry in self.error_titles['Titles']]:
                            self.append_content_data(directory=directory, filename='errors.json', new_content=new_title, content_key='Titles')
                    else:
                        final_title = results['Title'] + ' [' + results['Year'] + ']'
                        final_title = self.strip_bad_chars(title=final_title)  # Remove non-viable folder characters
                        if verbose:
                            print('Old Title: {title}'.format(title=title))
                            print('New Title: {new_title}'.format(new_title=new_title))
                            print('Final Title: {final_title}'.format(final_title=final_title))
                            print('Release Year: {release_year}'.format(release_year=release_year))
                            print('[RENAMING {old_title} to {new_title}]\n'.format(old_title=os.path.join(os.getcwd(), directory, title), new_title=os.path.join(os.getcwd(), directory, final_title)))
                        new_title = {
                            'original_filename': title,
                            'title': final_title,
                            'imdb_id': results['imdbID'],
                            'poster': results['Poster']
                        }
                        # Add the current formatted title to our "contents.json" index file:
                        self.append_content_data(directory=directory, filename='contents.json', new_content=new_title, content_key='Titles')
                        # Add the current full IMDb metadata to our "contents.json" index file:
                        self.append_content_data(directory=directory, filename='contents.json', new_content=results, content_key='Metadata')
                        if not self.debug:
                            # os.rename the folders to our newly formatted title:
                            old_path = os.path.join(directory, title)
                            new_path = os.path.join(directory, final_title)
                            os.rename(old_path, new_path)
                            print('{old_name} -> {new_name}'.format(old_name=title, new_name=final_title))
                            # Now, check the folder for files inside it and os.rename those too:                            
                            single_files = [f for f in os.listdir(new_path) if os.path.isfile(os.path.join(new_path, f))]
                            print(single_files)
                            for single_file in single_files:
                                old_file_path = os.path.join(new_path, single_file)
                                # print(old_file_path)
                                old_filename, ext = os.path.splitext(single_file)
                                # print(old_filename)
                                new_filename = final_title + ext
                                # print(new_filename)
                                new_file_path = os.path.join(new_path, new_filename)
                                # print(new_file_path)
                                os.rename(old_file_path, new_file_path)
                                print('[RENAMING] {old_path} to {new_path}....\n'.format(old_path=old_file_path, new_path=new_file_path))
                                if verbose:
                                    print('Old Filename: {old_filename}'.format(old_filename=old_filename))
                                    print('Old Filepath: {old_file_path}'.format(old_file_path=old_file_path))
                                    print('New Filename: {new_filename}'.format(new_filename=new_filename))
                                    print('New Filepath: {new_file_path}\n'.format(new_file_path=new_file_path))
                except Exception as error:
                    print("[ERROR]", error)
                    print('[FAILED] search terms: {search_terms}\n'.format(search_terms=new_title))
                    new_title = {
                        'original_filename': title,
                        'title': new_title
                    }
                    if title not in [entry['title'] if entry != [] else [] for entry in self.error_titles['Titles']]:
                        self.append_content_data(directory=directory, filename='errors.json', new_content=new_title, content_key='Titles')


if __name__ == '__main__':
    from datetime import datetime

    start = datetime.now()
    directory = os.path.join(os.getcwd(), 'test', 'data', 'Fake_Directory')
    directory = os.path.join(os.getcwd(), 'input')
    f = Formatter(directory=directory, debug=False, verbose=False)
    # directory = 'J:\Films'
    # f = Formatter(directory=directory, debug=True, verbose=False)
    finish = datetime.now() - start
    print("Finished in {total_time} seconds".format(total_time=finish))
