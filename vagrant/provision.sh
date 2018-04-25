#!/bin/bash

PROJECT_NAME=$1

PROJECT_DIR=/vagrant
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip

apt-get update -y
apt-get install -y unzip

# Create database
su - vagrant -c "createdb $PROJECT_NAME"

# Install Heroku
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install AWS CLI
rm -rf /tmp/awscli-bundle || true
rm -rf /tmp/awscli-bundle.zip || true
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "/tmp/awscli-bundle.zip"
unzip /tmp/awscli-bundle.zip -d /tmp
sudo /tmp/awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

# Virtualenv setup for project
su - vagrant -c "virtualenv --python=python3 $VIRTUALENV_DIR"
su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"


# Upgrade PIP itself
su - vagrant -c "$PIP install --upgrade pip"

# Upgrade setuptools (for example html5lib needs 1.8.5+)
su - vagrant -c "$PIP install --upgrade setuptools"

# Install PIP requirements
su - vagrant -c "$PIP install -r $PROJECT_DIR/requirements.txt"


# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PYTHONPATH=$PROJECT_DIR
export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev

alias dj="django-admin.py"
alias djrun="dj runserver 0.0.0.0:8000"

alias dokku="ssh -t dokku@staging.torchbox.com"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF
