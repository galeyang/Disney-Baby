# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json, urllib2, re, time

imdb_base_url = "http://www.imdb.com"
response = urllib2.urlopen(imdb_base_url+'/list/ls053060182/?start=1&view=compact&sort=listorian:asc&defaults=1&scb=0.04396881042336065')
# response = open('step1.html', 'rU') # temp: read local file for testing
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')


disney_char_list = []
for m in soup.find_all('tr', class_='list_item')[1:]:
    # print m
    movie_url = m.find(class_='title').a.get('href')
    title = m.find(class_='title').a.string
    year = m.find(class_='year').string
    rank = m.find(class_='user_rating').string

    response_cast = urllib2.urlopen(imdb_base_url + movie_url +'fullcredits?ref_=tt_cl_sm#cast')
    html_cast = response_cast.read().decode('utf-8')
    soup_cast = BeautifulSoup(html_cast, 'html.parser')

    for cast in soup_cast.find_all('td', class_='character'):
        # print cast
        for char in cast.find_all('a'):
            character = char.string
            # print character
            disney_char_list.append({"Title": title, "Movie URL": imdb_base_url+movie_url,"Year": year, "Rank": rank, "Character": character})

# print '\n'.join(map(str, disney_char_list))


with open ('disney_char_list.txt','w') as disney_char_fh:
    for row in json.dumps(disney_char_list):
        disney_char_fh.write(row)
