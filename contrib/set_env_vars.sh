#! /usr/bin/env bash

#
# Set the required environment variables. Call this script like this:
#  . ./contrib/set_env_vars.sh
#

export FLASK_APP=runserver.py
export FLASK_ENV=development
export STATS_CONFIG=production.py
