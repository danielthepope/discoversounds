from discoversounds.app import app
import pytest

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Discover Sounds' in response.data

def test_unknown_artist(client):
    response = client.get('/search?artist=sasdf&redirect=html')
    assert response.status_code == 200
    assert b'No results found' in response.data

def test_known_artist(client):
    response = client.get('/search?artist=Take+That&redirect=html')
    print(response.data)
    assert response.status_code == 200
    assert b'Looking for Take That' in response.data

def test_mix_of_artists(client):
    response = client.get('/search?artist=sasdf&artist=Take+That&redirect=html')
    assert response.status_code == 200
    assert b'Looking for sasdf, Take That' in response.data
