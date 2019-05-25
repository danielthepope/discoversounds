FROM python:3

WORKDIR /usr/src/app
# We copy just setup.py first to leverage Docker cache when installing requirements
COPY ./setup.py .
RUN pip install ".[prod,test]"

COPY . .
RUN pip install -e "."

EXPOSE 8000
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "discoversounds.app:app" ]
