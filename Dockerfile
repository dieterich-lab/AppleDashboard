FROM python:stretch

ADD . /app

RUN apt-get update && \
    apt-get install swig -y && \
    cd /app/ && \
    pip install pipenv && \
    pipenv install --ignore-pipfile --deploy --system

WORKDIR /app

ENV FLASK_ENV production
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV TZ=Europe/Berlin


EXPOSE 5424
EXPOSE 600

CMD [ "waitress-serve","--port", "600", "app:server" ]