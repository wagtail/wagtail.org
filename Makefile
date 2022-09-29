.PHONY: setup
setup: rebuild
	docker-compose run web django-admin migrate
	docker-compose run web django-admin createcachetable

.PHONY: rebuild
rebuild:
	bash -c "docker-compose build --build-arg UID=$$(id -u) --build-arg GID=$$(id -g)"

.PHONY: start
start:
	docker-compose up

.PHONY: runserver
runserver:
	docker-compose exec web django-admin runserver 0.0.0.0:8000

.PHONY: superuser
superuser:
	docker-compose run web django-admin createsuperuser

.PHONY: migrations
migrations:
	docker-compose run web django-admin makemigrations

.PHONY: migrate
migrate:
	docker-compose run web django-admin migrate

.PHONY: pull-production-data
pull-production-data:
	docker-compose run web fab pull_production_data

.PHONY: pull-production-media
pull-production-media:
	docker-compose run web fab pull_production_media

.PHONY: pull-staging-data
pull-staging-data:
	docker-compose run web fab pull_staging_data

.PHONY: rebuild
pull-staging-media:
	docker-compose run web fab pull_staging_media
