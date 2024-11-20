# Hosts and deployment

The site automatically deploys to its production and staging environments when pushing to the corresponding branches.

## Deployed environments

| Environment | Branch    | URL                            | Heroku                        |
| ----------- | --------- | ------------------------------ | ----------------------------- |
| Production  | `main`    | <https://wagtail.org/>         | e.g. `wagtail-org-production` |
| Staging     | `staging` | <https://staging.wagtail.org/> | e.g. `wagtail-org-staging`    |

## Login to Heroku

Please log in to Heroku before executing any Heroku CLI commands using the `heroku login -i` command.

## Connect to the shell

To open the shell of the servers.

```bash
fab staging-shell
fab production-shell
```

## Scheduled tasks

The following scheduled tasks are set up with Heroku Scheduler.

| Task                                 | Schedule              |
| ------------------------------------ | --------------------- |
| django-admin update_index            | Daily at 4:00 AM UTC  |
| django-admin publish_scheduled_pages | Every 10 minutes      |
| django-admin clearsessions           | Daily at 12:00 AM UTC |
| django-admin import_packages         | Daily at 3:00 AM UTC  |
| django-admin fetch_headless_issues   | Daily at 11:00 AM UTC |
