# -*- coding: utf-8 -*-
'''
Name: contents_creator.py
Author: Blair Gemmer
Version: 20170604

Description: 

Creates a contents.json files out of a given directory of films,

formatted in the following way: <movie_title> [<release_year>]

'''
import json
import os

import requests

films_directory = 'H:\Films'
contents_filename = 'contents.json'
contents_fullpath = os.path.join(films_directory, contents_filename)
films_list = os.listdir(films_directory)

# Set up the contents dictionary:
contents_dict = {}
contents_dict['Titles'] = []
contents_dict['Metadata'] = []
contents_dict['Total'] = 0

# Iterate through the films directory:
for film_title in films_list:
    # Split the title up by spaces to separate the title and release year:
    film_title_split = film_title.split(' ')
    # Grab all the words of the film title before the last element (the release year)
    film_title_words_array = film_title_split[0:-1]
    # If the film title has more than 1 word in it:
    if len(film_title_words_array) > 1:
        # Then grab all the words and join them by spaces:      
        film_title = ' '.join(film_title_words_array)
    else:
        film_title = film_title_words_array[0]
    # The release year is the last element in the list:
    release_year = film_title_split[-1]

    # Perform the OMDb API Request:
    payload = {
        't': film_title,
        'plot': 'Full',
        'r': 'json',
        'y': release_year,  # if release_year != '' else ''
        'apikey': '967174e1'
    }
    base_url = 'http://www.omdbapi.com/'
    response = requests.get(base_url, params=payload)
    if response.status_code == 200:
        try:
            response_json = response.json()
            title_data = {
                'poster': response_json['Poster'],
                'title': response_json['Title'],
                'imdb_id': response_json['imdbID']
            }
            contents_dict['Titles'].append(title_data)
            contents_dict['Metadata'].append(response_json)
            contents_dict['Total'] += 1
        except Exception as error:
            print('[ERROR]', error)
            print('\n')
            print('[REQUEST]')
            print(payload)
            print('\n')
            print('[RESPONSE]')
            print('\n')
            print(response)
            print('---------------------------')

# Finally, write all the gathered data to the contents file:
with open(contents_fullpath, mode='w') as outfile:
    json.dump(contents_dict, outfile)
