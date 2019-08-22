import os
import sys
import csv
import json
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    filename = 'film_sizes.json'

    with open(filename, 'r') as infile:
        # csv_reader = csv.reader(infile)
        # rows = []
        # first_pass = True
        # for row in csv_reader:
        #     if first_pass:
        #         header_row = row
        #         first_pass = False
        #     else:
        #         rows.append(row)
        film_data = json.load(infile)

    # print(json.dumps(data, indent=4))

    torrent_url = 'http://rarbg.to/torrents.php'

    # for film in film_data:
    film = film_data[0]
    query_param = '?search={imdb_id}+1080+aac'.format(imdb_id=film['imdb_id'])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    }

    response = requests.get(url=torrent_url + query_param, headers=headers)

    if response.status_code == 200:
        html_doc = response.content

        soup = BeautifulSoup(html_doc, 'html.parser')

        print(soup.prettify())
        # for td in soup.find_all('td'):
        #     if td.a is not None and td.a.get('title') is not None:
        #         # if 'aac' in td.a.get('title', '') and '1080' in td.a.get('title', ''):
        #         # print(td.a)
        #         print(td.a.get('title'))
        #         print('---\n')