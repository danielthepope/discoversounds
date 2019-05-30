from discoversounds.app import app
import pytest
import json
from pyquery import PyQuery

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Discover Sounds' in response.data

def test_unknown_artist_html(client):
    response = client.get('/search?artist=sasdf', headers={'Accept':'text/html'})
    assert response.status_code == 200
    assert b'No results found' in response.data

def test_unknown_artist_json(client):
    response = client.get('/search?artist=sasdf', headers={'Accept':'application/json'})
    assert response.status_code == 404
    assert b'No results found' in response.data

def test_known_artist(client):
    response = client.get('/search?artist=Take+That', headers={'Accept':'text/html'})
    print(response.data)
    assert response.status_code == 200
    assert b'Looking for Take That' in response.data

def test_mix_of_artists(client):
    response = client.get('/search?artist=sasdf&artist=Take+That', headers={'Accept':'text/html'})
    assert response.status_code == 200
    assert b'Looking for sasdf, Take That' in response.data

def test_accept_json(client):
    response = client.get('/search?artist=Take+That', headers={'Accept': 'application/json'})
    assert json.loads(response.data)

def test_accept_html(client):
    response = client.get('/search?artist=Take+That', headers={'Accept': 'text/html'})
    d = PyQuery(response.data)
    assert d('h1')

def test_no_accept_header(client):
    response = client.get('/search?artist=Take+That')
    d = PyQuery(response.data)
    assert d('h1')

def test_redirect(client):
    response = client.get('/search?artist=Take+That&redirect=Play+something+now')
    assert response.status_code == 302
    assert response.location.startswith('https://www.bbc.co.uk/sounds/play/')
    assert not response.location.endswith('/play/')
