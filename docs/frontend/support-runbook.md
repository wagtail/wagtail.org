# Support runbook

This document describes possible ways in which the system may fail or malfunction, with instructions how to handle and recover from these scenarios.

This runbook is supplementary to the [general 24/7 support runbook](https://intranet.torchbox.com/propositions/design-and-build-proposition/delivering-projects/dedicated-support-team/247-support-out-of-hours-runbook/), with details about project-specific actions which may be necessary for troubleshooting and restoring service.

See also our [incident process](https://intranet.torchbox.com/teams-and-practices/dedicated-support-team/hosting--and-application-support-retained-service/incident-process/) if you're not already following this.

## Contents

- [Scenario A: Site is down or returning 500 errors](#scenario-a-site-is-down-or-returning-500-errors)
- [Scenario B: Cloudflare CDN cache serving stale content](#scenario-b-cloudflare-cdn-cache-serving-stale-content)
- [Scenario C: Search returning no results or broken results](#scenario-c-search-returning-no-results-or-broken-results)
- [Scenario D: Scheduled tasks not running (Heroku Scheduler)](#scenario-d-scheduled-tasks-not-running-heroku-scheduler)
- [Scenario E: Packages page not updating (djangopackages.org import failing)](#scenario-e-packages-page-not-updating-djangopackagesorg-import-failing)
- [Scenario F: Roadmap page not updating (GitHub API failing)](#scenario-f-roadmap-page-not-updating-github-api-failing)
- [Scenario G: Newsletter sign-up form not working (Mailchimp)](#scenario-g-newsletter-sign-up-form-not-working-mailchimp)
- [Scenario H: Media (images or documents) not loading](#scenario-h-media-images-or-documents-not-loading)
- [Scenario I: Performance degradation](#scenario-i-performance-degradation)

## Scenario A: Site is down or returning 500 errors

### 1. Check Sentry for recent exceptions

Open the [Sentry project](https://torchbox.sentry.io/projects/wagtail-org/?project=1220804) and look for new or spiking error groups.

**Action if a specific exception is identified**

- Review the stack trace and breadcrumbs to understand the cause.
- Check whether a recent deployment triggered the issue:
  ```bash
  heroku releases -a wagtail-org-production
  ```
- Roll back if needed:
  ```bash
  heroku rollback -a wagtail-org-production
  ```

### 2. Check Heroku dynos and recent deployments

```bash
heroku ps -a wagtail-org-production
heroku releases -a wagtail-org-production
heroku logs --tail -a wagtail-org-production
```

Look for crashed dynos or failed release commands (e.g. failed migrations).

**Action if dynos are crashed**

- Restart dynos: `heroku restart -a wagtail-org-production`
- If a release command failed (e.g. migrations errored), investigate the log output and fix forward or roll back.

### 3. Check the database

Verify PostgreSQL is reachable and not at connection limits:

```bash
heroku pg:info -a wagtail-org-production
heroku pg:diagnose -a wagtail-org-production
```

**Action if the database is unavailable or at connection limit**

- Check Heroku Postgres status on the [Heroku status page](https://status.heroku.com/).
- If connection limit is reached, restart the app to recycle connections:
  ```bash
  heroku restart -a wagtail-org-production
  ```

### 4. Check Redis

The site uses Redis (Heroku Key-Value Store, Mini plan) for the application cache. If Redis is unavailable, the app falls back to the database cache automatically.

```bash
heroku redis:info -a wagtail-org-production
```

**Action if Redis is unavailable**

- The app will continue serving via database cache — no immediate user-facing impact.
- Monitor Heroku Redis status and await restoration.
- If the issue persists, remove or rotate the `REDIS_URL`/`REDIS_TLS_URL` env vars to force database cache until Redis is stable.

---

## Scenario B: Cloudflare CDN cache serving stale content

### 1. Check whether a Wagtail publish triggered a cache purge

Wagtail is configured to purge Cloudflare on page publish via `wagtail.contrib.frontend_cache`. If a published page is still showing old content, the purge may have failed.

Check Sentry or Heroku logs for `CloudflareBackend` errors at the time of publish.

**Action if the cache purge failed**

- Manually purge the affected URL(s) via the Cloudflare dashboard.
- Verify the environment variables are set correctly:
  - `FRONTEND_CACHE_CLOUDFLARE_EMAIL`
  - `FRONTEND_CACHE_CLOUDFLARE_TOKEN`
  - `FRONTEND_CACHE_CLOUDFLARE_ZONEID`

### 2. Check Cloudflare is not blocking legitimate traffic

If users report being blocked or seeing CAPTCHA challenges, check the Cloudflare Firewall Events dashboard for unexpected WAF rule matches.

**Action if Cloudflare is blocking legitimate traffic**

- Adjust WAF rules or temporarily set the affected path to "Bypass" in Cloudflare.
- Raise with the team lead before making permanent firewall changes.

---

## Scenario C: Search returning no results or broken results

### 1. Check whether the search index is up to date

Wagtail uses the database search backend. The index is rebuilt by a daily Heroku Scheduler task:

```
django-admin update_index — Daily at 4:00 AM UTC
```

Check whether the task ran successfully:

```bash
heroku logs --tail -a wagtail-org-production | grep update_index
```

**Action if the index is stale or the task failed**

- Manually rebuild the index:
  ```bash
  heroku run python manage.py update_index -a wagtail-org-production
  ```

### 2. Check for missing or unpublished content

If specific pages are missing from search results, verify they are published and not excluded from search in the Wagtail admin.

---

## Scenario D: Scheduled tasks not running (Heroku Scheduler)

The following tasks are configured in Heroku Scheduler:

| Task | Schedule |
|---|---|
| `django-admin update_index` | Daily at 4:00 AM UTC |
| `django-admin publish_scheduled_pages` | Every 10 minutes |
| `django-admin clearsessions` | Daily at 12:00 AM UTC |
| `django-admin import_packages` | Daily at 3:00 AM UTC |
| `django-admin fetch_headless_issues` | Daily at 11:00 AM UTC |

### 1. Verify the scheduler is configured

```bash
heroku addons:info scheduler -a wagtail-org-production
```

Open the Heroku Scheduler dashboard and confirm each task is listed with the correct schedule and command.

**Action if a task is missing or misconfigured**

- Re-add or correct the task via the Heroku Scheduler dashboard.
- Manually trigger the missed task:
  ```bash
  heroku run python manage.py <command_name> -a wagtail-org-production
  ```

### 2. Check logs for task errors

```bash
heroku logs --tail -a wagtail-org-production | grep -E "(update_index|publish_scheduled_pages|import_packages|fetch_headless_issues)"
```

---

## Scenario E: Packages page not updating (djangopackages.org import failing)

The `import_packages` task runs daily at 3:00 AM UTC, fetching Wagtail-related package data from `https://djangopackages.org/api/v4/grids/?q=wagtail`.

### 1. Check whether the external API is reachable

```bash
curl -I "https://djangopackages.org/api/v4/grids/?q=wagtail"
```

**Action if the API is unreachable or returning errors**

- Check Sentry for exceptions from `wagtailio.packages.views.process`.
- If djangopackages.org is having an outage, wait for service restoration. No action needed on our side.
- If the API response format has changed, a code change may be required.

### 2. Manually trigger an import

An admin can trigger the import from the Wagtail admin at Settings > **Django Packages** (`/admin/get-djangopackages/`) or via the management command:

```bash
heroku run python manage.py import_packages -a wagtail-org-production
```

---

## Scenario F: Roadmap page not updating (GitHub API failing)

The roadmap page displays open milestones from the [wagtail/roadmap](https://github.com/wagtail/roadmap) repository, fetched via the GitHub GraphQL API using the `GITHUB_ROADMAP_ACCESS_TOKEN` env var.

### 1. Check whether the GitHub token is valid

```bash
heroku config:get GITHUB_ROADMAP_ACCESS_TOKEN -a wagtail-org-production
```

Test the token manually:

```bash
curl -H "Authorization: Bearer <token>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/graphql \
  -d '{"query":"{ viewer { login } }"}'
```

**Action if the token is invalid or expired**

- Generate a new GitHub Personal Access Token with read-only access to the `wagtail/roadmap` repository.
- Update the config var:
  ```bash
  heroku config:set GITHUB_ROADMAP_ACCESS_TOKEN=<new_token> -a wagtail-org-production
  ```

### 2. Check for GitHub API rate limiting

The GraphQL API has a limit of 5,000 points per hour per token. A rate-limited response will contain an error with `type: "RATE_LIMITED"`.

**Action if rate limited**

- Wait for the rate limit window to reset.
- Review whether other automated tools are using the same token and exhausting the quota.

### 3. Manually trigger a roadmap import

An admin can trigger the import from the Wagtail admin at `/admin/roadmap/get-roadmap/`.

---

## Scenario G: Newsletter sign-up form not working (Mailchimp)

Newsletter sign-up forms embed Mailchimp's hosted form using `MAILCHIMP_ACCOUNT_ID` and `MAILCHIMP_NEWSLETTER_ID` env vars. These values are also stored per-snippet in the CMS via the `SignupFormSnippet` model (Wagtail admin: Snippets > Signup forms).

### 1. Check whether Mailchimp env vars and snippet values are set

```bash
heroku config -a wagtail-org-production | grep MAILCHIMP
```

Also verify the relevant `SignupFormSnippet` in the Wagtail admin has the correct Account ID and Audience ID populated.

**Action if env vars or snippet values are missing or incorrect**

- Update env vars via `heroku config:set`, or correct the snippet values directly in the Wagtail admin.

### 2. Check Mailchimp service status

Check [mailchimp.com/status](https://mailchimp.com/status/) for outages.

**Action if Mailchimp is down**

- No action required on our side. The embedded sign-up form will be unavailable until Mailchimp restores service.

---

## Scenario H: Media (images or documents) not loading

Media is stored in AWS S3. Production uses the `media.wagtail.org` bucket; staging uses `wagtailio-staging`.

### 1. Verify S3 configuration

```bash
heroku config -a wagtail-org-production | grep -E "AWS|S3"
```

Check that `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_STORAGE_BUCKET_NAME` are all set.

**Action if S3 credentials are invalid or missing**

- Retrieve or generate IAM credentials from the AWS console.
- Update the Heroku config vars.

### 2. Check S3 bucket accessibility

```bash
aws s3 ls s3://media.wagtail.org
```

**Action if bucket is inaccessible**

- Review the S3 bucket policy and IAM permissions.
- Engage a sysadmin or AWS account holder if access changes are required.

### 3. Check for missing image renditions

If original images exist in S3 but aren't displaying, renditions may not have been generated. Wagtail generates renditions on first request; a mass-regeneration can be triggered if needed:

```bash
heroku run python manage.py wagtail_update_image_renditions -a wagtail-org-production
```

---

## Scenario I: Performance degradation

### 1. Check Scout APM

Review [Scout APM](https://scoutapm.com/) for slow transactions, N+1 queries, or memory growth following a recent deployment.

### 2. Check DebugBear

Review [DebugBear lab tests](https://www.debugbear.com/project/25758?interval=month&share=SABlYrvo9gP5234W5TMmANCgD) for frontend performance or accessibility regressions.

### 3. Check Heroku dyno metrics

```bash
heroku ps -a wagtail-org-production
heroku logs --tail -a wagtail-org-production | grep -E "Error R14|Error R15"
```

R14/R15 errors indicate memory quota exceeded.

**Action if memory pressure is high**

- Check for memory leaks introduced by recent deployments.
- Restart dynos to reclaim memory: `heroku restart -a wagtail-org-production`
- Scale up the dyno type temporarily via the Heroku dashboard if restarts don't help.

### 4. Check Redis cache health

A cold or unavailable Redis cache will increase database load significantly.

```bash
heroku redis:info -a wagtail-org-production
```

**Action if cache hit rate is very low**

- A recent deployment may have changed cache key structure, causing a cold cache warm-up period.
- Cache warms naturally as traffic hits the site — no manual action is needed unless the database is overwhelmed.
- If database load is critical, restart the app and monitor Scout APM for query volume.
