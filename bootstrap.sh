#!/usr/bin/env bash

echo "Environment installation is beginning. This may take a few minutes.."



# Script to set up dependencies for Django on Vagrant.
PGSQL_VERSION=9.4

# Need to fix locale so that Postgres creates databases in UTF-8
locale-gen en_GB.UTF-8
dpkg-reconfigure locales

export LANGUAGE=en_GB.UTF-8
export LANG=en_GB.UTF-8
export LC_ALL=en_GB.UTF-8



apt-get update -y

apt-get install -y build-essential python python-dev python-setuptools python-pip

# Git (we'd rather avoid people keeping credentials for git commits in the repo, but sometimes we need it for pip requirements that aren't in PyPI)
apt-get install -y git

# Postgresql
if ! command -v psql; then
    apt-get install -y postgresql-$PGSQL_VERSION libpq-dev
fi

##
#	Setup the database
##

echo "Configuring postgres.."
sudo -u postgres psql -c "create user timez with password 'timez';"
sudo -u postgres psql -c "create database timez;"
sudo -u postgres psql -c "grant all privileges on database timez to timez;"


##
#   Setup dev environment
##

BASEDIR='/vagrant/'

echo "Configuring python"
cd $BASEDIR
pip install -r requirments.txt
python manage.py migrate
python populate.py