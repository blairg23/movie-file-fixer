import requests, json, re

def search_title(url='http://www.omdbapi.com/', search_terms='', release_year='', verbose=False):
		'''
		Searches OMDB api for a movie title closest to the given string.
		'''
		payload = {
			't': search_terms,
			'plot': 'Full',
			'r': 'json',
			'y': release_year #if release_year != '' else ''
		}		
		req = requests.get(url=url, params=payload)
		if req.status_code == 200:
			response = json.loads(req.content)
			if response['Response'] == "True": # If the response was successful (if we found a movie title)
				if verbose:					
					print '[SUCCESSFUL] search terms: {search_terms}\n'.format(search_terms=search_terms)
					print json.dumps(response, indent=4), '\n'
				return response # Return the full response
			else: # Otherwise, remove the last word from the title (in case it's a junk word or a year of release),
				search_terms = ' '.join(search_terms.split(' ')[:-1])
				if verbose:
					print '[FAILED] new search terms: {search_terms}\n'.format(search_terms=search_terms)
				return search_title(search_terms=search_terms, release_year=release_year, verbose=verbose) # And recursively try again				

def find_release_year(title=None, verbose=False):
		'''
		Returns the best candidate for the release year for the given title by removing the improbable candidates.
		'''		
		year_list = re.findall(r"\d{4}", title) # Find all possible "release year" candidates

		if len(year_list) > 0: # If we found any results:
			if verbose:
				print 'Release Year Candidates: {year_list}'.format(year_list=year_list)
			removal_list = []
			for year in year_list:
				if int(year) < 1900: # We won't be dealing with movies before the 1900's
					removal_list.append(str(year))
			for remove_string in removal_list: # For each string that matches the removal process,
				year_list.remove(remove_string) # Remove that string		

			# Add only the last one as that is the most likely candidate of a real candidate (this won't be true when resolutions are at 4K)		
			release_year = year_list[-1] # This will also be the only candidate if there is only one candidate

			if verbose:
				print 'Best Guess for Release Year: {release_year}'.format(release_year=release_year)
			return release_year
		else:
			return ''

titles = [
			'Howl\'s Moving Castle (2004) 720p', 
			'Ferris Bueller\'s Day Off (1986) [1080p]',
			'I Hope They Serve Beer In Hell [2009] DvDrip H.264 AAC',
			"You.Don't.Mess.With.The.Zohan[2008][Unrated.Edition]DvDrip-aXXo"
]


final_titles = []
for title in titles:
	print 'Old Title', title
	#print search_title(search_terms=title, verbose=True), '\n'
	release_year = find_release_year(title=title)
	new_title = " ".join(map(str.title, re.findall(r"\w+|\w+'\w+|\w+-\w+|\w+|[(#$!)]+|'\w+", title)))
	max_size = 8
	if len(new_title.split(' ')) > max_size:
		new_title = " ".join(new_title.split(' ')[0:max_size])	
	if " \'S" in new_title:
		new_title = new_title.replace(" \'S", "\'s")
	if " \'T" in new_title:
		new_title = new_title.replace(" \'T", "\'t")
	print 'New Title', new_title
	searched_title = search_title(search_terms=new_title, release_year=release_year, verbose=True)		
	#print searched_title['Title']
	print 'Final Title', searched_title
	final_titles.append(searched_title['Title'] + '[' + release_year + ']')
print final_titles