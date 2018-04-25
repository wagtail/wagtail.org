.PHONY: clean_local_database \
		\
		pull_staging_data push_staging_data pull_staging_media \
		push_staging_media clean_staging_database deploy_staging \
		staging_shell \
		\
		setup_production deploy_production pull_production_data \
		push_production_data production_shell pull_production_media \
		push_production_media

staging_remote = dokku@staging.torchbox.com
staging_db_instance = wagtailio
staging_instance = wagtailio
staging_container = wagtailio.web.1
production_instance = wagtailio-production
local_db_name = wagtailio
local_media = /vagrant/media/

error:
	@echo "Please choose the correct target"

# Local commands
clean_local_database:
	sudo -u postgres psql  -d wagtailio -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Staging commands
pull_staging_data: clean_local_database
	ssh -t $(staging_remote) postgres:export $(staging_db_instance) | pg_restore -d $(local_db_name)

push_staging_data: clean_staging_database
	ssh -t $(staging_remote) ps:stop $(staging_instance) && \
	(pg_dump -Fc --no-acl --no-owner -w $(local_db_name) | ssh -t $(staging_remote) postgres:import $(staging_db_instance) || true) && \
	ssh -t $(staging_remote) ps:start $(staging_instance)

pull_staging_media:
	HOST_STRING=$(staging_remote) rsync -av --delete --blocking-io -e docker/dokku_rsync.sh \
		$(staging_container):`ssh $(staging_remote) run $(staging_instance) printenv CFG_MEDIA_DIR` \
		$(local_media)

push_staging_media:
	HOST_STRING=$(staging_remote) rsync -av --delete --blocking-io -e docker/dokku_rsync.sh \
		$(local_media) \
		$(staging_container):`ssh $(staging_remote) run $(staging_instance) printenv CFG_MEDIA_DIR`

clean_staging_database:
	echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" | ssh -t $(staging_remote) postgres:connect $(staging_db_instance)

deploy_staging:
	git push $(staging_remote):$(staging_instance) staging:staging

staging_shell:
	ssh -t $(staging_remote) enter $(staging_instance)


# Production commands
setup_production:
	heroku git:remote -a $(production_instance) -r heroku-production

deploy_production: setup_production
	git push heroku-production master:master

pull_production_data:clean_local_database
	heroku pg:pull --app $(production_instance) DATABASE_URL $(local_db_name)

push_production_data:
	heroku pg:push --app $(production_instance) $(local_db_name) DATABASE_URL

pull_production_media:
	AWS_ACCESS_KEY_ID=`heroku config:get --app $(production_instance) BUCKETEER_AWS_ACCESS_KEY_ID` \
	AWS_SECRET_ACCESS_KEY=`heroku config:get --app $(production_instance) BUCKETEER_AWS_SECRET_ACCESS_KEY` \
	aws s3 sync --delete s3://`heroku config:get --app $(production_instance) BUCKETEER_BUCKET_NAME` $(local_media)

push_production_media:
	AWS_ACCESS_KEY_ID=`heroku config:get --app $(production_instance) BUCKETEER_AWS_ACCESS_KEY_ID` \
	AWS_SECRET_ACCESS_KEY=`heroku config:get --app $(production_instance) BUCKETEER_AWS_SECRET_ACCESS_KEY` \
	aws s3 sync --delete $(local_media) s3://`heroku config:get --app $(production_instance) BUCKETEER_BUCKET_NAME`

production_shell: setup_production
	heroku run bash
