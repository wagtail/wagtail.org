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

sh:	## Enter the web container
	docker-compose exec web bash

runserver:	## 🏃 - Run Django server
	docker-compose exec web django-admin runserver 0.0.0.0:8000

superuser:	## 🔒 - Create superuser
	docker-compose run web django-admin createsuperuser

migrations:	## 🧳 - Make migrations
	docker-compose run web django-admin makemigrations

migrate:  ## 🧳 - Migrate
	docker-compose run web django-admin migrate

dumpfixtures:  # 📦 - Dump fixtures
	docker-compose run web django-admin dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.rendition -e sessions -e wagtailsearch.indexentry -e wagtailcore.referenceindex -e wagtailcore.pagesubscription -e wagtailcore.workflowcontenttype -e wagtailadmin.editingsession > fixtures/wagtail.org-demo.json
	npx prettier --write fixtures/wagtail.org-demo.json

load_initial_data:  # 📦 - Load initial data
	docker-compose run web django-admin load_initial_data
