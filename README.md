# Discover Sounds

This is a pile of very hacky Python code made for a BBC hack day.

Given any number of artists to search for, this service will find a radio show available on BBC Sounds that contains songs by most of those artists. For example, if you search for Ramones, The Chemical Brothers and Jamie T, you might be presented with [this show from Steve Lamacq](https://www.bbc.co.uk/programmes/m0002785).

## Installation

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How do I run it?

If you have an alternative data source for `shows.csv` and `show_to_artist.csv`, put their location in a file called `.env`. The file could look something like this:

```
SHOWS_CSV=data/shows.csv
SHOW_TO_ARTIST_CSV=data/vpid_to_artist.csv
```

Start the server using

```
python server.py
```

The server runs on port 5002 by default. This can be overridden by setting the environment variable `PORT` in the `.env` file.
