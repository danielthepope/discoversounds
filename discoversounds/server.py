from dotenv import load_dotenv
load_dotenv()

import collections
import os
import random
from functools import reduce
from string import Template

from flask import Flask, Response, jsonify, redirect, render_template, request
from flask_restful import Api, Resource
from sqlalchemy import not_

from discoversounds.database import db_session
from discoversounds.helpers import sanitise_artist, set_interval, timeit
from discoversounds.models import Show, ShowToArtist


app = Flask(__name__, static_folder='../public', static_url_path='')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

programmes_url = Template('https://www.bbc.co.uk/programmes/$show')


ARTIST_KEYS = []
ARTIST_NAMES = {}


@timeit
def update_artists():
    global ARTIST_KEYS
    global ARTIST_NAMES
    all_artists = list([a[0] for a in db_session().query(ShowToArtist.artist).all()])
    db_session.remove()

    artist_representations = dict()
    for artist in all_artists:
        sanitised_artist = sanitise_artist(artist)
        if sanitised_artist in artist_representations:
            artist_representations[sanitised_artist].append(artist)
        else:
            artist_representations[sanitised_artist] = list([artist])
    ARTIST_KEYS = artist_representations.keys()
    for key in ARTIST_KEYS:
        ARTIST_NAMES[key] = [a[0] for a in collections.Counter(artist_representations[key]).most_common()]


class Search(Resource):
    def get(self):
        artists_query = [a for a in request.args.getlist('artist') if a != '']
        redir = request.args.get('redirect')
        print('Looking for ' + str(artists_query))
        results = find_shows(artists_query)
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
        return find_artists(term)


@timeit
def find_artists(term):
    sanitised = sanitise_artist(term)
    return sorted([ARTIST_NAMES[a][0] for a in ARTIST_KEYS if sanitised in a])[0:20]


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@timeit
def find_shows(artists_query):
    sanitised_query = set(map(sanitise_artist, artists_query))
    full_artist_names = reduce(list.__add__, [ARTIST_NAMES[key] for key in sanitised_query])
    vpids_and_artist = ShowToArtist.query.filter(
        ShowToArtist.artist.in_(full_artist_names)).all()
    if len(vpids_and_artist) == 0:
        return []
    just_vpids = [a.vpid for a in vpids_and_artist]
    counter = collections.Counter(just_vpids)
    count = max(counter.values())
    good_vpids = [counter_result for counter_result in counter.items() if counter_result[1] == count][0:10]  # Up to 10 of the best matches
    response = list()
    for counter_result in good_vpids:
        show = counter_result[0]
        extra_info = {
            'artists': [a.artist for a in vpids_and_artist if a.vpid == show],
            'other_artists': [a[0] for a in db_session().query(ShowToArtist.artist).filter(ShowToArtist.vpid == show, not_(ShowToArtist.artist.in_(full_artist_names))).all()],
            'count': count,
            'programmes_url': programmes_url.substitute({'show': show}),
        }
        response.append(
            {**db_session().query(Show).get(show).__dict__, **extra_info})
    print([result['programmes_url'] for result in response])
    return response


if __name__ == '__main__':
    api = Api(app)
    api.add_resource(Search, '/search')
    api.add_resource(Artists, '/artists')

    set_interval(update_artists, 600)
    update_artists()
    port = os.getenv('PORT') or 5002
    print('PORT', port)
    host = os.getenv('HOST') or '127.0.0.1'
    print('HOST', host)
    app.run(port=port, host=host)
