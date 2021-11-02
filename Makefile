.PHONY: setup rebuild start superuser migrations migrate

setup:
	make rebuild
	docker-compose run web django-admin migrate
	docker-compose run web django-admin createcachetable

rebuild:
	bash -c "docker-compose build --build-arg UID=$$(id -u) --build-arg DOCKER_GID=$$(ls -ln /var/run/docker.sock | awk '{print $$4}')"

start:
	docker-compose up

superuser:
	docker-compose run web django-admin createsuperuser

migrations:
	docker-compose run web django-admin migrations

migrate:
	docker-compose run web django-admin migrate
