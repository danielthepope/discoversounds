FROM python:3.7-alpine

WORKDIR /usr/src/app
# We copy just setup.py first to leverage Docker cache when installing requirements
COPY ./setup.py .
RUN pip install ".[prod]"

COPY . .
RUN pip install -e "."

ENV PYTHONUNBUFFERED TRUE
ENV REFRESH_DATA TRUE
EXPOSE 8000
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "discoversounds.app:app" ]
