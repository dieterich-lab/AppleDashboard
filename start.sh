#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# enviroment variables
export FLASK_ENV=development
export FLASK_APP=app.py

export POSTGRES_USER=test
export POSTGRES_PASSWORD=test
export POSTGRES_DB=example
export POSTGRES_PORT=5425
export POSTGRES_HOST=localhost

# run flask
flask run --host=0.0.0.0 --no-reload