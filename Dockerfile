FROM python:3

WORKDIR /usr/src/app
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002
ENTRYPOINT [ "python", "server.py" ]
