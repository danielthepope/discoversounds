FROM python:3

WORKDIR /usr/src/app
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install "."

ENV HOST=0.0.0.0
EXPOSE 5002
ENTRYPOINT [ "python", "-u", "discoversounds/server.py" ]
