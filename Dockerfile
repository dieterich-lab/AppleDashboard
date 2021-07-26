FROM python:slim

ADD . /app
COPY . /app

RUN apt-get update && \
    apt-get install swig -y && \
    cd /app/ && \
    pip install pipenv && \
    pipenv install --ignore-pipfile --deploy --system

WORKDIR /app

ENV FLASK_ENV production
ENV FLASK_APP index.py
ENV TZ=Europe/Berlin


EXPOSE 5424
EXPOSE 600

CMD ["waitress-serve","--port", "600","index:app.server" ]