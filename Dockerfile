FROM nikolaik/python-nodejs:python3.7-nodejs14-alpine

WORKDIR /usr/src/app
# We copy just setup.py first to leverage Docker cache when installing requirements
COPY ./setup.py .
RUN pip install ".[prod]"
COPY ./frontend/package* ./frontend/
WORKDIR /usr/src/app/frontend
RUN npm install
WORKDIR /usr/src/app


COPY . .
RUN pip install -e "."
WORKDIR /usr/src/app/frontend
RUN npm run build
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED TRUE
ENV REFRESH_DATA TRUE
EXPOSE 8000
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "discoversounds.app:app" ]
