# Wagtail.org

This is the source code to [Wagtail's website](https://wagtail.org)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/wagtail/wagtail.org)

## Requirements

-   Docker or Vagrant (see below)
-   [Fabric](https://www.fabfile.org/), [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (only for downloading production / staging data)

## Installation (Docker Compose)

You first need to install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/). Once they are installed, run the following commands to get up and running:

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

Then, to start the development server, open a new terminal window and run:

```
make runserver
```

This will launch `django-admin runserver` in the web container, which serves Wagtail on http://localhost:8000/

To run migrations within Docker you'll need to run:

```
make migrate
```

### Creating a superuser

To create a new superuser locally, run:

```
make superuser
```
To login with Wagtail, please redirect to http://localhost:8000/admin/

### Pulling production data / media

If you'd like to work with production data and have access, run the following commands:

```
fab pull-production-data
fab pull-production-media
```

Access will only be given when absolutely necessary.

## Installation (Vagrant)

You first need to install [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/). Once they are installed, run the following commands to get up and running:

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

## Frontend tooling

To install and build the frontend:

-   `nvm use` to use the suggested node version (requires [nvm](https://github.com/nvm-sh/nvm), [fnm](https://github.com/Schniz/fnm) or similar. You'll also need to run `nvm install` to install and activate the version of node required for the project)
-   `npm i` to install dependcies
-   `npm run build` to compile CSS & JS

Other common commands:

-   `npm run start` start the Webpack build in watch mode, without live-reload
-   `npm run start:reload` start the Webpack server build on port 3000 with live-reload
-   `npm run lint` lint JS & CSS files
-   `npm run format` format files

For more info see [Frontend general info](docs/frontend/general-info.md)

## Deployment

The site is hosted on Heroku, and is deployed automatically. `main` deploys to production, and `staging` deploys to staging.

## docs.wagtail.org

Wagtail documentation is hosted at [readthedocs](https://readthedocs.org/). A Cloudflare worker is in place to rewrite canonical URLs on old versions of the documentation - see `conf/wagtaildocs-cloudflare-worker.js`.
