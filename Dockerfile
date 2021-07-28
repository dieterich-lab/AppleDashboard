FROM python:slim as base


COPY . /app
COPY Pipfile Pipfile.lock /app/

RUN apt-get update && \
    apt-get install -y && \
    cd /app/ && \
    pip install --no-cache-dir pipenv && \
    pipenv install --ignore-pipfile --deploy --system --clear

# Runtime image from here
FROM base

WORKDIR /app

# Copy node_modules from builder image
COPY --from=base /app .
ADD . /app

ENV FLASK_ENV production
ENV FLASK_APP index.py
ENV TZ=Europe/Berlin

EXPOSE 5424
EXPOSE 600

CMD ["waitress-serve","--port", "600","index:app.server" ]