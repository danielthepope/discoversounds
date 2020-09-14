from dotenv import load_dotenv
load_dotenv()

import collections
from datetime import datetime
import logging as log
import os
import random
from string import Template

from flask import Flask, Response, jsonify, redirect, render_template, request
from flask_restful import Api, Resource
from sqlalchemy import not_

from discoversounds.database import db_session, init_db
from discoversounds.helpers import sanitise_artist, set_interval, timeit
from discoversounds.models import Artist, ArtistRelation, Show, ShowToArtist, Service

log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=log.DEBUG)

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

PROGRAMMES_URL = Template('https://www.bbc.co.uk/programmes/$show')
SOUNDS_URL = Template('https://www.bbc.co.uk/sounds/play/$show')
IMAGE_URL = Template('https://ichef.bbci.co.uk/images/ic/160x90/$ipid.jpg')

ARTIST_KEYS = []
ARTIST_NAMES = {}
SERVICES = {}
STATS = {}


@timeit
def update_artists():
    global ARTIST_KEYS
    global ARTIST_NAMES
    all_artists = [a.artist_name for a in Artist.query.all()]
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
        names = [a[0] for a in collections.Counter(artist_representations[key]).most_common()]
        popularity = len(artist_representations[key])
        ARTIST_NAMES[key] = (names, popularity)


@timeit
def update_services():
    global SERVICES
    all_services = Service.query.all()
    indexed_services = {}
    for service in all_services:
        indexed_services[service.sid] = service
    SERVICES = indexed_services
    db_session.remove()


@timeit
def update_stats():
    global STATS
    rs = db_session().execute('select shows.availability_from from shows order by availability_from desc limit 1')
    for row in rs:
        last_update = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        STATS['last_update'] = last_update.strftime('%d %b %Y %H:%M')
    rs = db_session().execute('select count(vpid) from shows where has_songs = 1')
    for row in rs:
        STATS['show_count'] = row[0]
    STATS['artist_count'] = len(ARTIST_KEYS)
    db_session.remove()


def update():
    update_artists()
    update_services()
    update_stats()


class Search(Resource):
    def get(self):
        artists_query = [a for a in request.args.getlist('artist') if a != '']
        include_local = request.args.get('includelocal')
        output_type = request.headers.get('Accept')
        log.info('Looking for %s', str(artists_query))
        results = find_shows(artists_query, include_local)
        # Return JSON
        if output_type == 'application/json':
            if len(results) == 0:
                return 'No results found', 404
            return jsonify(results)
        # Redirect to Sounds
        if request.args.get('redirect') and len(results) > 0:
            return redirect(random.choice(results)['sounds_url'])
        # Return HTML
        return Response(render_template('results.html', results=results, artists_query=artists_query,
                                        include_local=include_local), mimetype='text/html')


class Artists(Resource):
    def get(self):
        term = request.args.get('term')
        if len(term) < 2:
            return [], 404
        return find_artists(term)


@timeit
def find_artists(term):
    sanitised = sanitise_artist(term)
    all_matches = [ARTIST_NAMES[a] for a in ARTIST_KEYS if sanitised in a]
    # Sort by popularity
    all_matches.sort(key=lambda a: a[1], reverse=True)
    return [a[0][0] for a in all_matches][0:15]


@app.route('/')
def index():
    return Response(render_template('index.html', stats=STATS, include_local=True), mimetype='text/html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def expand_artist_names(artists_query):
    sanitised_query = set(map(sanitise_artist, artists_query))
    full_artist_names = list()
    for key in sanitised_query:
        if key in ARTIST_NAMES:
            full_artist_names += ARTIST_NAMES[key][0]
        else:
            full_artist_names.append(key)
    return full_artist_names


def generate_response(shows_to_display, vpids_and_artist, full_artist_names):
    response = list()
    for show in shows_to_display:
        vpid = show.vpid
        display_item = {
            'artists': [Artist.query.get(a.artist).artist_name for a in vpids_and_artist if a.vpid == vpid],
            'other_artists': [Artist.query.get(a[0]).artist_name for a in db_session().query(ShowToArtist.artist)
                              .filter(ShowToArtist.vpid == vpid, not_(ShowToArtist.artist.in_(full_artist_names))).all()],
            'programmes_url': PROGRAMMES_URL.substitute({'show': show.epid}),
            'sounds_url': SOUNDS_URL.substitute({'show': show.epid}),
            'image_url': IMAGE_URL.substitute({'ipid': show.ipid}),
            'availability_from': show.availability_from.strftime('%d %b'),
            'availability_to': show.availability_to,
            'synopsis': show.synopsis,
            'sid': show.sid in SERVICES and SERVICES[show.sid].name or show.sid,
            'title': show.title,
            'vpid': show.vpid,
        }
        response.append(display_item)
    return response


@timeit
def find_shows(artists_query, include_local):
    full_artist_names = expand_artist_names(artists_query)
    artists = [Artist.query.filter(Artist.artist_name == name).first() for name in full_artist_names]
    artist_ids = [a.artist_id for a in artists if a]
    vpids_and_artist = ShowToArtist.query.filter(ShowToArtist.artist.in_(artist_ids)).all()
    if len(vpids_and_artist) == 0:
        return []
    just_vpids = [a.vpid for a in vpids_and_artist]
    counter = collections.Counter(just_vpids)
    count = max(counter.values())
    good_vpids = [counter_result for counter_result in counter.items() if counter_result[1] == count]
    good_shows = [Show.query.get(vpid[0]) for vpid in good_vpids]
    if not include_local:
        good_shows = [s for s in good_shows if (s.sid not in SERVICES or not SERVICES[s.sid].local)]
    good_shows.sort(key=lambda show: show.availability_from, reverse=True)
    shows_to_display = good_shows[0:10]  # Up to 10 of the best matches
    response = generate_response(shows_to_display, vpids_and_artist, full_artist_names)
    log.info([result['programmes_url'] for result in response])
    return response


api = Api(app)
api.add_resource(Search, '/search')
api.add_resource(Artists, '/artists')
init_db()

if os.getenv('REFRESH_DATA'):
    log.info('Updating data every 5 minutes')
    set_interval(update, 300)
else:
    log.warning('REFRESH_DATA is not set: artists only collected once')
update()

if __name__ == '__main__':
    port = os.getenv('PORT') or 5002
    log.info('PORT %s', port)
    host = os.getenv('HOST') or '127.0.0.1'
    log.info('HOST %s', host)
    app.run(port=port, host=host)
