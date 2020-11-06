#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


export POSTGRES_USER=test
export POSTGRES_PASSWORD=test
export POSTGRES_DB=example
export POSTGRES_PORT=5425
export POSTGRES_HOST=localhost

# run flask
python app.py

