# Wagtail.org

This is the source code to [Wagtail's website](https://wagtail.org)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/wagtail/wagtail.org)

## Installation (Docker Compose)

You firstly need to install [git](https://git-scm.com), [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/). Once they are installed, run the following commands to get up and running:

```
git clone https://github.com/wagtail/wagtail.org.git
cd wagtail.org
make setup
```

This will create a set of Docker containers on your local machine and also create a blank database.

### Starting the development environment

Run the following command to start the Docker containers:

```
make start
```

Then, to start the development server, run:

```
make runserver
```

This will launch `django-admin runserver` in the web container, which serves Wagtail on http://localhost:8000/

### Creating a superuser

To create a new superuser locally, run:

```
make superuser
```

### Pulling production data / media

If you'd like to work with production data and have access, run the following commands:

```
make pull-production-data
make pull-production-media
```

(you will be prompted to log in to Heroku both times. To log in, hit enter when it asks you and copy and paste the URL it gives you into a browser)

## Installation (Vagrant)

You firstly need to install [git](https://git-scm.com), [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/). Once they are installed, run the following commands to get up and running:

```
git clone https://github.com/wagtail/wagtail.org.git
cd wagtail.org
vagrant up
```

This will download the base image and provision a local VM that will run the site locally.

You will need to apply migrations, create a super user, and create a cache table once the vagrant environment is setup.

```
vagrant ssh
./manage.py migrate
./manage.py createsuperuser
./manage.py createcachetable
```

## Usage (Vagrant)

Common Vagrant commands:

-   `vagrant up` starts the VM
-   `vagrant halt` stops the VM
-   `vagrant ssh` opens a shell in the VM
-   `vagrant destroy` deletes the VM

Shortcut commands:

Within the VM shell, you can run `./manage.py` to run any Django management command. But we have added a couple of shortcuts to save on typing:

-   `dj <command> [args]` - Runs a management command (eg, `dj shell`)
-   `djrun` - Starts the webserver on port 8000

## Deployment

The site is hosted on heroku, and is deployed by pushing to the heroku remote.

Creating and pushing to the heroku branch is handled automatically by fabric command.

To staging

`fab deploy_staging`

To production

`fab deploy_production`

## docs.wagtail.org

Wagtail documentation is hosted at [readthedocs](https://readthedocs.org/). A Cloudflare worker is in place to rewrite canonical URLs on old versions of the documentation - see `conf/wagtaildocs-cloudflare-worker.js`.
