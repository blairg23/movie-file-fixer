import requests
import os
import json


def fix_JSON(json_message=None):
	result = None
	try:		
		result = json.loads(json_message)
	except Exception as e:		
		# Find the offending character index:
		idx_to_replace = int(e.message.split(' ')[-1].replace(')',''))		
		# Remove the offending character:
		json_message = list(json_message)
		json_message[idx_to_replace] = ' '
		new_message = ''.join(json_message)		
		return fix_JSON(json_message=new_message)
	return result


base_url = 'http://www.omdbapi.com/'
tv_series = {}
films = {}
episodes = {}
games = {}

for i in range(1, 9999999):
	imdb_id = 'tt' + str(i).zfill(7)
	#imdb_id = 'tt0120690'
	print imdb_id



	payload = {
				'i':imdb_id,
				'plot':'full',
				'r':'json'		
	}
	try:
		response = requests.get(base_url, params=payload)
		if response.status_code == 200:		
			result = None
			result = fix_JSON(json_message=response.content)

			if result != None:
				if result['Response'] != 'False':
					if result['Type'] == 'movie':
						films[result['Title']] = result
					elif result['Type'] == 'series':
						tv_series[result['Title']] = result
					elif result['Type'] == 'episode':
						episodes[result['Title']] = result
					elif result['Type'] == 'game':
						games[result['Title']] = result
					else:
				
						print '[ERROR] Type:', result['Type']
	except ConnectionError as e:
		break

with open('tv_series.json', 'w') as tv_series_outfile:
	json.dump(tv_series, tv_series_outfile)

with open('films.json', 'w') as films_outfile:
	json.dump(films, films_outfile)

with open('episodes.json', 'w') as episodes_outfile:
	json.dump(episodes, episodes_outfile)

with open('games.json', 'w') as games_outfile:
	json.dump(games, games_outfile)