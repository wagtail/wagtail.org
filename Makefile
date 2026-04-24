# ----------------------------------------------------------------------------
# Self-Documented Makefile
# ref: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# ----------------------------------------------------------------------------
.PHONY: help
.DEFAULT_GOAL := help

help:  ## ⁉️  - Display help comments for each make command
	@grep -E '^[0-9a-zA-Z_-]+:.*? .*$$'  \
		$(MAKEFILE_LIST)  \
		| awk 'BEGIN { FS=":.*?## " }; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'  \
		| sort

setup: build  ## 🔨 - Set instance up
	docker compose run --rm web django-admin migrate
	docker compose run --rm web django-admin createcachetable

build:  ## 🔨 - Build Docker container
	docker compose build --build-arg UID=$$(id -u) --build-arg GID=$$(id -g)

start:	## 🎬 - Start containers
	docker compose up

sh:	## Enter the web container
	docker compose exec web bash

runserver:	## 🏃 - Run Django server
	docker compose exec web bash -c "DJANGO_RUNSERVER_HIDE_WARNING=true django-admin runserver 0.0.0.0:8000"

superuser:	## 🔒 - Create superuser
	docker compose run --rm web django-admin createsuperuser

migrations:	## 🧳 - Make migrations
	docker compose run --rm web django-admin makemigrations

migrate:  ## 🧳 - Migrate
	docker compose run --rm web django-admin migrate
