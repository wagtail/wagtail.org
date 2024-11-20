# wagtail.org — Data Protection

This page gives an overview of potentially-sensitive data stored or processed by the wagtail.org project.

## Data locations

### Logical location of data

All in the Django-managed Postgres database.

### Physical location of data

The Heroku databases are stored in the EU region on AWS, as are all of the Heroku addons. The exception is database backups – see [Heroku Postgres Production Tier Technical Characterization](https://devcenter.heroku.com/articles/heroku-postgres-production-tier-technical-characterization#data-encryption).

### Exports

All exports include the above data. The first steps when downloading a copy of the production database, or cloning it to staging, should be to delete all records in the user-submitted tables:

```bash
$ python manage.py shell
>>> from wagtail.contrib.forms.models import FormSubmission
>>> FormSubmission.objects.all().delete()
```

When copying the data to staging, decide whether to leave user accounts intact: delete them if users are members of the public, don't if they're stakeholders who will still want to access the staging site. If using the data locally, you should anonymise user accounts:

```bash
$ python manage.py shell
>>> from wagtail.users.models import User
>>> for user in User.objects.all():
...     user.first_name = "User"
...     user.last_name = user.id
...     user.email = f"user.{user.id}@example.com"
...     user.username = f"user.{user.id}"
...     user.save()
```

## Responding to GDPR requests

If a request is received to purge or report the stored data for a given user:

-   For user account data, delete the user from the Wagtail admin
-   For form submissions, search the submissions and delete if necessary using the Django shell.
