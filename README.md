# Wagtail.org

This is the source code to [Wagtail's website](https://wagtail.org)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/wagtail/wagtail.org)

If you use the gitpod development environment these commands are run at startup.

```bash
fab build
fab migrate
fab start
```

# Setting up a local build

This repository includes `docker-compose` configuration for running the project in local Docker containers,
and a fabfile for provisioning and managing this.

There are a number of other commands to help with development using the fabric script. To see them all, run:

```bash
fab -l
```

## Dependencies

The following are required to run the local environment. The minimum versions specified are confirmed to be working:
if you have older versions already installed they _may_ work, but are not guaranteed to do so.

- [Docker](https://www.docker.com/), version 19.0.0 or up
  - [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) installer
  - [Docker Engine for Linux](https://hub.docker.com/search?q=&type=edition&offering=community&sort=updated_at&order=desc&operating_system=linux) installers
- [Docker Compose](https://docs.docker.com/compose/), version 1.24.0 or up
  - [Install instructions](https://docs.docker.com/compose/install/) (Linux-only: Compose is already installed for Mac users as part of Docker Desktop.)
- [Fabric](https://www.fabfile.org/), version 2.4.0 or up
  - [Install instructions](https://www.fabfile.org/installing.html)
- Python, version 3.6.9 or up

Note that on Mac OS, if you have an older version of fabric installed, you may need to uninstall the old one and then install the new version with pip3:

```bash
pip uninstall fabric
pip3 install fabric
```

You can manage different python versions by setting up `pyenv`: https://realpython.com/intro-to-pyenv/

Additionally, for interacting with production / staging environments, you'll need:

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

## Running the local build for the first time

If you are using Docker Desktop, ensure the Resources:File Sharing settings allow the cloned directory to be mounted in the web container (avoiding `mounting` OCI runtime failures at the end of the build step).

Starting a local build can be done by running:

```bash
git clone git@github.com:wagtail/wagtail.org.git
cd wagtail.org
fab build
fab migrate
fab start
```

This will start the containers in the background, but not Django. To do this, connect to the web container with `fab sh` and run `honcho start` to start both Django and the Webpack dev server in the foreground.

Then, connect to the running container again (`fab sh`) and:

```bash
dj createcachetable
dj createsuperuser
```

The site should be available on the host machine at: http://127.0.0.1:8000/

If you only wish to run the frontend or backend tooling, the commands `honcho` runs are in `docker/Procfile`.

### Pulling production data / media

If you'd like to work with production data and have access, run the following commands:

```
fab pull-production-data
fab pull-production-media
```

(you will be prompted to log in to Heroku both times. To log in, hit enter when it asks you and copy and paste the URL it gives you into a browser)

## Deployment

To deploy the application to staging / production:

Make sure you have access to the relevant app on Heroku. Ask a Torchbox admin if you require access.

Also make sure you are logged in:

```sh
heroku login -i
```

### Deploying to staging

Run the following command to add a git remote called heroku-staging:

```sh
heroku git:remote -a wagtailio-staging -r heroku-staging
```

Now push your local staging branch to the heroku remote:

```sh
git push heroku-staging staging:master
```

### Deploying to production

Run the following command to add a git remote called heroku-production:

```sh
heroku git:remote -a wagtailio-production -r heroku-production
```

Now push your local production branch to the heroku remote:

```sh
git push heroku-production production:master
```

## Installing python packages

Python packages can be installed using `poetry` in the web container:

```
fab sh
poetry add wagtail-guide
```

To reset installed dependencies back to how they are in the `poetry.lock` file:

```
fab sh
poetry install --no-root
```

## docs.wagtail.org

Wagtail documentation is hosted at [readthedocs](https://readthedocs.org/). A Cloudflare worker is in place to rewrite canonical URLs on old versions of the documentation - see `conf/wagtaildocs-cloudflare-worker.js`.
