FROM python:3.7-slim

WORKDIR /app
COPY Pipfile Pipfile.lock ./


RUN apt-get update && \
    apt-get install -y && \
    cd /app/ && \
    pip install --no-cache-dir pipenv && \
    pipenv install --ignore-pipfile --deploy --system --clear &&\
    rm -rf /var/lib/apt/lists/*



COPY . /app

ENV FLASK_ENV production
ENV TZ=Europe/Berlin

EXPOSE 5424
EXPOSE 600

CMD ["waitress-serve","--port", "600","index:app.server" ]
