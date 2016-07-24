# -*- coding: utf-8 -*-
'''
Name: contents_checker.py
Author: Blair Gemmer
Version: 20160723

Description: 

Checks the contents.json for any possible errors.

'''

import os
import json

contents_file_directory = 'J:\\to_sort'
contents_filename = 'contents.json'
contents_fullpath = os.path.join(contents_file_directory, contents_filename)

films_directory = 'J:\Films'
films_list = os.listdir(films_directory)
film_titles = []

with open(contents_fullpath) as infile:
	indexed_titles = json.load(infile)


# First, check our contents file against our film directory:
for indexed_title in indexed_titles['Titles']:
	film_title = indexed_title['title']
	film_titles.append(film_title)
	if film_title not in films_list:
		print film_title

# Second, check our film directory against our contents file:
for film_title in films_list:
	if film_title not in film_titles:
		print film_title