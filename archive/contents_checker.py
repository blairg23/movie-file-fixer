# -*- coding: utf-8 -*-
'''
Name: contents_checker.py
Author: Blair Gemmer
Version: 20170521

Description: 

Checks the contents.json for any possible errors.

'''

import json
import os

contents_file_directory = 'H:\\Films'
contents_filename = 'contents.json'
contents_fullpath = os.path.join(contents_file_directory, contents_filename)

films_directory = 'H:\Films'
films_list = [filename for filename in os.listdir(films_directory) if filename != contents_filename]
film_titles = []

with open(contents_fullpath, encoding='utf-8') as infile:
    indexed_titles = json.load(infile)

# First, check our contents file against our film directory:
for indexed_title in indexed_titles['Titles']:
    film_title = indexed_title['title']
    film_titles.append(film_title)
    if film_title not in films_list:
        print(film_title)

# Second, check our film directory against our contents file:
for film_title in films_list:
    if film_title not in film_titles:
        print(film_title)
