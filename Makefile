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
	docker-compose run web django-admin migrate
	docker-compose run web django-admin createcachetable

build:  ## 🔨 - Build Docker container
	bash -c "docker-compose build --build-arg UID=$$(id -u) --build-arg GID=$$(id -g)"

start:	## 🎬 - Start containers
	docker-compose up

runserver:	## 🏃 - Run Django server
	docker-compose exec web django-admin runserver 0.0.0.0:8000

superuser:	## 🔒 - Create superuser
	docker-compose run web django-admin createsuperuser

migrations:	## 🧳 - Make migrations
	docker-compose run web django-admin makemigrations

migrate:  ## 🧳 - Migrate
	docker-compose run web django-admin migrate

pull-production-data:	## ⬇️ - Pull production data
	docker-compose run web fab pull_production_data

pull-production-media:	## 📸 - Pull production media
	docker-compose run web fab pull_production_media

pull-staging-data:	## ⬇️ - Pull production data
	docker-compose run web fab pull_staging_data

pull-staging-media:	## 📸 - Pull production media
	docker-compose run web fab pull_staging_media
