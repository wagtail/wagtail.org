.PHONY: setup rebuild start superuser migrations migrate pull-production-data pull-production-media pull-staging-data pull-staging-media

setup:
	make rebuild
	docker-compose run web django-admin migrate
	docker-compose run web django-admin createcachetable

rebuild:
	bash -c "docker-compose build --build-arg UID=$$(id -u) --build-arg DOCKER_GID=$$(ls -ln /var/run/docker.sock | awk '{print $$4}')"

start:
	docker-compose up

runserver:
	docker-compose exec web django-admin runserver 0.0.0.0:8000

superuser:
	docker-compose run web django-admin createsuperuser

migrations:
	docker-compose run web django-admin migrations

migrate:
	docker-compose run web django-admin migrate

pull-production-data:
	docker-compose run web fab pull_production_data

pull-production-media:
	docker-compose run web fab pull_production_media

pull-staging-data:
	docker-compose run web fab pull_staging_data

pull-staging-media:
	docker-compose run web fab pull_staging_media
