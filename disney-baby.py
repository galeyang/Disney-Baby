# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from itertools import groupby
from operator import itemgetter
import json, urllib2, os.path, pprint, csv

import plotly
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go

# pre-define fuction ---

# Crawl IMDb website to get disney animation character list
def crawl_disney_char():

    imdb_base_url = 'http://www.imdb.com'
    response = urllib2.urlopen(imdb_base_url+'/list/ls053060182/?start=1&view=compact&sort=listorian:asc&defaults=1&scb=0.04396881042336065')

    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    disney_char_list = []
    for m in soup.find_all('tr', class_='list_item')[1:]:

        movie_url = m.find(class_='title').a.get('href')
        title = m.find(class_='title').a.string
        year = m.find(class_='year').string
        if year <= 2015:
            break

        rank = m.find(class_='user_rating').string

        response_cast = urllib2.urlopen(imdb_base_url + movie_url +'fullcredits?ref_=tt_cl_sm#cast')
        html_cast = response_cast.read().decode('utf-8')
        soup_cast = BeautifulSoup(html_cast, 'html.parser')

        for cast in soup_cast.find_all('td', class_='character'):

            for char in cast.find_all('a'):
                character = char.string
                
                disney_char_list.append({'Title': title, 'Movie URL': imdb_base_url+movie_url,'Year': year, 'Rank': rank, 'Character': character})

    # print '\n'.join(map(str, disney_char_list))

    with open ('disney_char_list.json','w') as disney_char_fh:
        for row in json.dumps(disney_char_list):
            disney_char_fh.write(row)

# Check if baby's name co-exist in Disney characters' name
def in_charlist(name, charlist):
    for c in charlist:
        if name == c['Character']:
            return True
    return False


# Clean the baby name from folder and join with Disney characters
def clean_disney_baby():

    with open('disney_char_list.json', 'rU') as disney_char_fh:
        disney_char_list = json.loads(disney_char_fh.read())

    babyname_list = []
    years = xrange(1923,2016)

    for year in years:
        name_fh = open('names/yob'+ str(year) + '.txt', 'rU')

        for row in name_fh: 
            row = row.strip().split(',')

            if in_charlist(row[0], disney_char_list):
                # babyname_list.append({'Year': year, 'Name': row[0],'Gender': row[1], 'Count': row[2]})
                babyname_list.append({'Year': year, 'Name': [row[0],row[1]], 'Count': row[2]})

        name_fh.close()

        print '\n'.join(map(str, babyname_list))

    with open ('disney_baby_list.json','w') as disney_baby_fh:
        for row in json.dumps(babyname_list):
            disney_baby_fh.write(row)

# Find top N trendy disney baby name by the sum of counts
def find_top_name(no_top):

    with open('disney_baby_list.json', 'rU') as disney_baby_fh:
        disney_baby_list = json.loads(disney_baby_fh.read())

    grouper = itemgetter('Name')
    counts_byname = []

    for key, grp in groupby(sorted(disney_baby_list, key = grouper), grouper):

        temp_dict = {'Name': key}
        temp_dict['Sum'] = sum(int(item['Count']) for item in grp)
        # print temp_dict
        counts_byname.append(temp_dict)

    top_name = sorted(counts_byname, key = lambda x : x['Sum'], reverse=True)[:no_top]

    top_name_list = [row['Name'][0] for row in top_name]
    # pprint.pprint(top_name)
    # print [row['Name'] for row in top_name]

    with open ('top_name.json','w') as top_ten_fh:
        for row in json.dumps(top_name):
            top_ten_fh.write(row)

# Generate csv file for visualization
def final_generate_csv():

    with open('disney_char_list.json', 'rU') as disney_char_fh:
        disney_char_list = json.loads(disney_char_fh.read())

    with open('disney_baby_list.json', 'rU') as disney_baby_fh:
        disney_baby_list = json.loads(disney_baby_fh.read())

    with open('top_name.json', 'rU') as top_ten_fh:
        top_name = json.loads(top_ten_fh.read())

    # Name, Gender, BornYear, Count
    # James, M, 30430430, 1923

    top_count = 1

    for name in top_name:
        data_name_c = [['Name','Gender', 'BornYear', 'Count']]
        for year in xrange(1923,2016):
            for row in disney_baby_list: 
                if row['Name'] == name['Name'] and row['Year'] == year:

                   data_name_c.append([name['Name'][0],  name['Name'][1], year, row['Count']]) 

                   with open('output/top_name' + str(top_count) + '.csv', 'wb') as csvfile:
                        writer = csv.writer(csvfile)
                        for row in data_name_c:
                            writer.writerow(row)

        top_count += 1


    # Name, movie-title, movie-year
    # James, LionKing, 1982
    # James, Fish, 2010

    data_name_movie = [["Name", "Movie Title", "Year", "Rank"]]
    for name in top_name:
        for row in disney_char_list:
            if name['Name'][0] == row['Character']:
                data_name_movie.append([name['Name'][0], row['Title'], row['Year'], row['Rank']])

    with open('output/name_movie_mapping.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in data_name_movie:
            writer.writerow(row)


# end of pre-define fuction ---

# define the number of top name
no_top = 5*4

if os.path.exists('disney_char_list.json') is False:
    crawl_disney_char()

if os.path.exists('disney_baby_list.json') is False:
    clean_disney_baby()

if os.path.exists('top_name.json') is False:
    find_top_name(no_top)

if os.path.exists('output/top_name1.csv') is False:
    final_generate_csv()


trace = {}
trace_movie = {}

with open('output/name_movie_mapping.csv', 'rb') as f_movie:
    reader_movie = csv.reader(f_movie)
    dat_name_movie = list(reader_movie)

for i in xrange(1,no_top+1):

    with open('output/top_name'+ str(i) + '.csv', 'rb') as f:
        reader = csv.reader(f)
        dat_top_name = list(reader)

    if dat_top_name[1][1] == "F":

        trace[i] = go.Scatter(
              x=[row[2] for row in dat_top_name],
              y=[row[3] for row in dat_top_name],
              fill='tozeroy',
              fillcolor="rgba(236, 172, 160, 1)",
              line=dict(width=0.5,
                  color='#666666')
        )

    else:
        trace[i] = go.Scatter(
              x=[row[2] for row in dat_top_name],
              y=[row[3] for row in dat_top_name],
              fill='tozeroy',
              fillcolor="rgba(146, 190, 212, 1.00)",
              line=dict(width=0.5,
                  color='#666666')
        )

    for row_movie in dat_name_movie:
        if row_movie[0] == dat_top_name[1][0]:

            for row_name in dat_top_name:
                if row_movie[2] == row_name[2]:
                    movie_y = row_name[3]

            if dat_top_name[1][1] == "F":

                trace_movie[i] = go.Scatter(
                    x = [row_movie[2]],
                    y = [movie_y],
                    mode = 'markers',
                    marker=dict(
                        color='#b7513e',
                        symbol='circle',
                        size=9,
                    ),
                    text= 'Movie: '+row_movie[1]+'| IMDb Rank: ' + row_movie[3]
                )
            else:
                trace_movie[i] = go.Scatter(
                    x = [row_movie[2]],
                    y = [movie_y],
                    mode = 'markers',
                    marker=dict(
                        color='#0e74a7',
                        symbol='circle',
                        size=9,
                    ),
                    text= 'Movie: '+row_movie[1]+'| IMDb Rank: ' + row_movie[3]
                )

with open('top_name.json', 'rU') as top_ten_fh:
    top_name = json.loads(top_ten_fh.read())

# top_name_list = [row['Name'][0] +", "+ row['Name'][1] for row in top_name]

top_rank = 1
top_name_list = []

for row in top_name:
    top_name_list.append(str(top_rank) + ". " + row['Name'][0] +", "+ row['Name'][1])
    top_rank +=1

fig = tools.make_subplots(
    rows=no_top/5, 
    cols=5, 
    subplot_titles=top_name_list, 
    vertical_spacing=0.1)

fig_c = 1
for row in xrange (1,no_top/5+1):
    for col in xrange(1, 6):
        fig.append_trace(trace[fig_c], row, col)
        fig.append_trace(trace_movie[fig_c], row, col)
        fig_c += 1


fig['layout'].update(
    height=700, 
    width=1200, 
    title="The Most Trendy Baby Names Inspired by Disney characters in US History",
    showlegend=False,
    plot_bgcolor="#f7f7f7",
    # plot_bgcolor="rgba(146, 190, 212, 0.4)"
)


for i in xrange(1,no_top+1):

    fig['layout']['xaxis'+str(i)].update(
            titlefont=dict(
                size= 10,
                color='rgb(82, 82, 82)',
            ),
            showgrid=False, 
            showline=False,
            ticks='outside',
            tickcolor='rgb(204, 204, 204)',
            tickwidth=1,
            ticklen=5,
            tickfont=dict(
                size= 10,
                color='rgb(82, 82, 82)',
            )
        )

    fig['layout']['yaxis'+str(i)].update(
            showgrid=False,
            zeroline=False,
            showline=False,
            # showticklabels=False,
            tickfont=dict(
                size= 10,
                color='rgb(82, 82, 82)',
            )
        )

    fig['layout']['annotations'][i-1].update(
        font=dict(
                size= 12,
                color='rgb(82, 82, 82)',
        )
    )

plotly.offline.plot(fig, filename = 'linechart.html')


