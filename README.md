# Discover Sounds

This is a pile of very hacky Python code made for a BBC hack day.

Given any number of artists to search for, this service will find a radio show available on BBC Sounds that contains songs by most of those artists. For example, if you search for Ramones, The Chemical Brothers and Jamie T, you might be presented with [this show from Steve Lamacq](https://www.bbc.co.uk/programmes/m0002785).

## Installation

```
virtualenv venv
source venv/bin/activate
pip install -e "."
```

### Other dependencies

If running in production, running tests or editing the code, you'll want to install other optional dependencies.

```
pip install -e ".[dev,test,prod]"
```

## How do I run it?

If you have an alternative data source for `radio-sample.db`, put its connection string in a file called `.env`. The file could look something like this:

```
DATABASE=sqlite:///data/radio.db
```

Start the server using

```
python discoversounds/app.py
```

The server runs on port 5002 by default. This can be overridden by setting the environment variable `PORT` in the `.env` file.

### Running in production

You can run gunicorn if you installed the `prod` optional dependencies.

```
gunicorn --bind 127.0.0.1:8000 discoversounds.app:app
```

This will run it on localhost port 8000.

## How is the database updated?

In production, another script polls the Sounds API to keep the database updated with new shows. That bit is in a private repo.
