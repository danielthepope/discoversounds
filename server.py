from dotenv import load_dotenv
load_dotenv()

import collections
import csv
import json
import os
import random
import time
from string import Template

from flask import Flask, Response, jsonify, redirect, render_template, request
from flask_restful import Api, Resource

app = Flask(__name__, static_folder='public', static_url_path='')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
api = Api(app)

SHOWS_CSV = os.getenv('SHOWS_CSV') or 'shows.sample.csv'
SHOW_TO_ARTIST_CSV = os.getenv('SHOW_TO_ARTIST_CSV') or 'show_to_artist.sample.csv'

SHOW_TO_ARTIST_ROWS = list()
PROGRAMME_DETAILS = dict()
ARTISTS_BY_SHOW = dict()
ARTISTS = set()

programmes_url = Template('https://www.bbc.co.uk/programmes/$show')

def sanitise_artist(artist):
    return artist.lower().replace('the ','').replace(' ','').replace('.', '')

# Initialise data
start = time.time()
with open(SHOW_TO_ARTIST_CSV, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        SHOW_TO_ARTIST_ROWS.append({
            'show': row['vpid'],
            'artist': row['artist'],
            'sanitised_artist': sanitise_artist(row['artist'])
        })
        if row['vpid'] not in ARTISTS_BY_SHOW:
            ARTISTS_BY_SHOW[row['vpid']] = []
        ARTISTS_BY_SHOW[row['vpid']].append(row['artist'])
        ARTISTS.add(row['artist'])

with open(SHOWS_CSV, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        entry = dict()
        entry['show'] = row['up_version_pid']
        entry['title'] = row['up_programme_name']
        entry['service'] = row['up_service_id']
        PROGRAMME_DETAILS[row['up_version_pid']] = entry

end = time.time()
print('Loaded data in ' + str(round(end - start, 3)) + ' seconds')

class Search(Resource):
    def get(self):
        artists_query = [a for a in request.args.getlist('artist') if a != '']
        redir = request.args.get('redirect')
        print('Looking for ' + str(artists_query))
        results = search(artists_query)
        if redir == 'html':
            return Response(render_template('results.html', results=results, artists_query=artists_query), mimetype='text/html')
        if len(results) == 0:
            return 'No results found', 404
        if redir == 'programmes':
            return redirect(random.choice(results)['programmes_url'])
        return jsonify(results)

class Artists(Resource):
    def get(self):
        term = request.args.get('term')
        if len(term) < 4:
            return [], 404
        return sorted([a for a in ARTISTS if term.lower() in a.lower()])[0:20]

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

def search(artists_query):
    sanitised_query = set(map(sanitise_artist, artists_query))
    vpids_and_artist = [row for row in SHOW_TO_ARTIST_ROWS if row['sanitised_artist'] in sanitised_query]
    if len(vpids_and_artist) == 0:
        return []
    just_vpids = [a['show'] for a in vpids_and_artist]
    counter = collections.Counter(just_vpids)
    count = max(counter.values())
    good_vpids = [counter_result for counter_result in counter.items() if counter_result[1] == count][0:10] # Up to 10 of the best matches
    response = list()
    for counter_result in good_vpids:
        show = counter_result[0]
        extra_info = {
            'artists': [a['artist'] for a in vpids_and_artist if a['show'] == show],
            'other_artists': [a for a in ARTISTS_BY_SHOW[show] if sanitise_artist(a) not in sanitised_query],
            'count': count,
            'programmes_url': programmes_url.substitute({'show': show}),
        }
        response.append({**PROGRAMME_DETAILS[show], **extra_info})
    print([result['programmes_url'] for result in response])
    return response

api.add_resource(Search, '/search')
api.add_resource(Artists, '/artists')

if __name__ == '__main__':
    app.run(port=os.getenv('PORT') or 5002, host='0.0.0.0')
