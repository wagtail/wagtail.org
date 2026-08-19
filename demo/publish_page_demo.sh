#!/usr/bin/env bash
#
# Demo: create and publish a wagtailio.blog.BlogPage via the Wagtail 8.0
# REST API v3, running against the local wagtail.org dev environment.
#
# Requires: curl, jq
#
# Usage:
#   TOKEN=wagtail_xxx PARENT_ID=5 ./publish_page_demo.sh
#   TOKEN=wagtail_xxx PARENT_ID=5 ./publish_page_demo.sh --one-step
#
# TOKEN     API token from `./manage.py api_tokens create --user=<you> --name=demo`
# PARENT_ID id of an existing blog.BlogIndexPage, e.g. from:
#           curl -s -H "Authorization: Bearer $TOKEN" \
#             "$API_ROOT/pages/?type=blog.BlogIndexPage&fields=id,title" | jq

set -euo pipefail

API_ROOT="${API_ROOT:-http://localhost:8000/api/v3-preview}"
SITE_ROOT="${SITE_ROOT:-http://localhost:8000}"
ONE_STEP=false

if [[ "${1:-}" == "--one-step" ]]; then
  ONE_STEP=true
fi

: "${TOKEN:?Set TOKEN to an API token (see: ./manage.py api_tokens create --user=<you> --name=demo)}"
: "${PARENT_ID:?Set PARENT_ID to the id of a blog.BlogIndexPage}"

auth=(-H "Authorization: Bearer $TOKEN")
json=(-H "Content-Type: application/json")

step() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }

step "1. Confirm the token works (whoami)"
curl -sf "${auth[@]}" "$API_ROOT/whoami/" | jq .

slug="rest-api-demo-$(date +%s)"
today="$(date +%Y-%m-%d)"

if [[ "$ONE_STEP" == true ]]; then
  step "2. Create + publish blog.BlogPage in one call (meta.action=publish)"
  create_body=$(jq -n --argjson parent_id "$PARENT_ID" --arg slug "$slug" --arg date "$today" '{
    meta: {type: "blog.BlogPage", parent_id: $parent_id, action: "publish"},
    title: "REST API one-step demo",
    slug: $slug,
    introduction: "Published in a single POST via the v3 API.",
    date: $date,
    body: [{type: "paragraph", value: "<p>Hello from the REST API (one-step publish).</p>"}]
  }')
  response=$(curl -sf "${auth[@]}" "${json[@]}" -X POST "$API_ROOT/pages/" -d "$create_body")
  echo "$response" | jq .
  page_id=$(echo "$response" | jq -r .id)

  step "3. View it live"
  echo "Open: $SITE_ROOT/blog/$slug/"
  exit 0
fi

step "2. Create a draft blog.BlogPage (no action = draft only)"
create_body=$(jq -n --argjson parent_id "$PARENT_ID" --arg slug "$slug" --arg date "$today" '{
  meta: {type: "blog.BlogPage", parent_id: $parent_id},
  title: "REST API demo post",
  slug: $slug,
  introduction: "Created as a draft via the v3 API, then published via actions/publish/.",
  date: $date,
  body: [{type: "paragraph", value: "<p>Hello from the REST API!</p>"}]
}')
response=$(curl -sf "${auth[@]}" "${json[@]}" -X POST "$API_ROOT/pages/" -d "$create_body")
echo "$response" | jq .
page_id=$(echo "$response" | jq -r .id)
echo "Created draft page id=$page_id, slug=$slug"

step "3. Confirm it isn't live yet"
echo "Requesting front end URL (expect a 404): $SITE_ROOT/blog/$slug/"
curl -s -o /dev/null -w 'HTTP %{http_code}\n' "$SITE_ROOT/blog/$slug/"

step "4. Publish it"
curl -sf "${auth[@]}" -X POST "$API_ROOT/pages/$page_id/actions/publish/" | jq .

step "5. Confirm it's live"
echo "Requesting front end URL again (expect a 200): $SITE_ROOT/blog/$slug/"
curl -s -o /dev/null -w 'HTTP %{http_code}\n' "$SITE_ROOT/blog/$slug/"
echo "Open in your browser: $SITE_ROOT/blog/$slug/"
