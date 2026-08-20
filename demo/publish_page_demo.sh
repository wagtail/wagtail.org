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
# TOKEN       API token from `./manage.py api_tokens create --user=<you> --name=demo`
# PARENT_ID   id of an existing blog.BlogIndexPage, e.g. from:
#             curl -s -H "Authorization: Bearer $TOKEN" \
#               "$API_ROOT/pages/?type=blog.BlogIndexPage&fields=id,title" | jq
# AUTHOR_ID   id of a blog.Author snippet (defaults to 131, "Meagen Voss")
# CATEGORY_ID id of a taxonomy.Category (defaults to 1, "News")
# MAIN_IMAGE_FILE path to a local image file to upload for main_image
#             (defaults to ./demo/wagtail.webp)
# BODY_IMAGE_FILE path to a local image file to upload for the body's
#             inline image block (defaults to ./demo/peregrinefalcon.webp)
# COLLECTION_ID id of a wagtailcore.Collection to upload the images into
#             (defaults to 1, the root collection)

set -euo pipefail

API_ROOT="${API_ROOT:-http://localhost:8000/api/v3-preview}"
SITE_ROOT="${SITE_ROOT:-http://localhost:8000}"
AUTHOR_ID="${AUTHOR_ID:-131}"  # blog.Author "Meagen Voss"
CATEGORY_ID="${CATEGORY_ID:-1}"  # taxonomy.Category "News"
MAIN_IMAGE_FILE="${MAIN_IMAGE_FILE:-./demo/wagtail.webp}"
BODY_IMAGE_FILE="${BODY_IMAGE_FILE:-./demo/peregrinefalcon.webp}"
COLLECTION_ID="${COLLECTION_ID:-1}"  # wagtailcore.Collection to upload into
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

step "2. Upload images"
main_image_response=$(curl -sf "${auth[@]}" -F "file=@${MAIN_IMAGE_FILE}" -F "title=Wagtail on the ground" -F "collection_id=${COLLECTION_ID}" "$API_ROOT/images/")
echo "$main_image_response" | jq .
main_image_id=$(echo "$main_image_response" | jq -r .id)
echo "Uploaded main image id=$main_image_id"

body_image_response=$(curl -sf "${auth[@]}" -F "file=@${BODY_IMAGE_FILE}" -F "title=Peregrine falcon" -F "collection_id=${COLLECTION_ID}" "$API_ROOT/images/")
echo "$body_image_response" | jq .
body_image_id=$(echo "$body_image_response" | jq -r .id)
echo "Uploaded body image id=$body_image_id"

slug="fun-facts-about-birds-$(date +%s)"
today="$(date +%Y-%m-%d)"

# Real StoryBlock content (h2/h3 headings + paragraph rich text, plus an
# inline image block), so the demo page reads like an actual blog post
# rather than placeholder text.
body=$(jq -n --argjson image_id "$body_image_id" '[
  {"type": "paragraph", "value": "<p>Birds have been quietly pulling off some of the animal kingdom'"'"'s most outrageous feats for millions of years. Here are a few facts that might make you look twice at the next pigeon you see.</p>"},
  {"type": "h2", "value": "Speed demons of the sky"},
  {"type": "paragraph", "value": "<p>The peregrine falcon is the fastest animal on Earth, reaching over 240 mph (390 km/h) in a hunting dive. No bat, cheetah, or fighter jet pilot pulling a stunt comes close.</p>"},
  {"type": "image", "value": {"image": $image_id, "decorative": false, "alt_text": "A peregrine falcon mid-dive"}},
  {"type": "h2", "value": "Tiny but mighty"},
  {"type": "paragraph", "value": "<p>The bee hummingbird, the smallest bird alive, weighs less than a penny. Its heart can beat over 1,200 times per minute mid-flight, and it can hover in place indefinitely thanks to a figure-eight wing motion.</p>"},
  {"type": "h2", "value": "Brainy birds"},
  {"type": "paragraph", "value": "<p>Crows and ravens can recognize individual human faces years later, hold grudges, and craft tools from twigs and wire to solve puzzles. Some corvids even appear to plan ahead, a trait once thought unique to great apes.</p>"},
  {"type": "h3", "value": "One more quick fact"},
  {"type": "paragraph", "value": "<p>Owls can rotate their necks up to 270 degrees because their eyes are fixed in their sockets and can'"'"'t move on their own.</p>"}
]')

if [[ "$ONE_STEP" == true ]]; then
  step "3. Create + publish blog.BlogPage in one call (meta.action=publish)"
  create_body=$(jq -n --argjson parent_id "$PARENT_ID" --arg slug "$slug" --arg date "$today" --argjson body "$body" --argjson author_id "$AUTHOR_ID" --argjson category_id "$CATEGORY_ID" --argjson main_image_id "$main_image_id" '{
    meta: {type: "blog.BlogPage", parent_id: $parent_id, action: "publish"},
    title: "Fun Facts About Birds",
    slug: $slug,
    introduction: "A quick dive into some of the strangest and most delightful things birds can do.",
    date: $date,
    category_id: $category_id,
    authors: [{author_id: $author_id}],
    main_image_id: $main_image_id,
    body: $body
  }')
  response=$(curl -sf "${auth[@]}" "${json[@]}" -X POST "$API_ROOT/pages/" -d "$create_body")
  echo "$response" | jq .
  page_id=$(echo "$response" | jq -r .id)

  step "4. View it live"
  echo "Open: $SITE_ROOT/blog/$slug/"
  exit 0
fi

step "3. Create a draft blog.BlogPage (no action = draft only)"
create_body=$(jq -n --argjson parent_id "$PARENT_ID" --arg slug "$slug" --arg date "$today" --argjson body "$body" --argjson author_id "$AUTHOR_ID" --argjson category_id "$CATEGORY_ID" --argjson main_image_id "$main_image_id" '{
  meta: {type: "blog.BlogPage", parent_id: $parent_id},
  title: "Fun Facts About Birds",
  slug: $slug,
  introduction: "A quick dive into some of the strangest and most delightful things birds can do.",
  date: $date,
  category_id: $category_id,
  authors: [{author_id: $author_id}],
  main_image_id: $main_image_id,
  body: $body
}')
response=$(curl -sf "${auth[@]}" "${json[@]}" -X POST "$API_ROOT/pages/" -d "$create_body")
echo "$response" | jq .
page_id=$(echo "$response" | jq -r .id)
echo "Created draft page id=$page_id, slug=$slug"

step "4. Confirm it isn't live yet"
echo "Requesting front end URL (expect a 404): $SITE_ROOT/blog/$slug/"
curl -s -o /dev/null -w 'HTTP %{http_code}\n' "$SITE_ROOT/blog/$slug/"

step "5. Publish it"
curl -sf "${auth[@]}" -X POST "$API_ROOT/pages/$page_id/actions/publish/" | jq .

step "6. Confirm it's live"
echo "Requesting front end URL again (expect a 200): $SITE_ROOT/blog/$slug/"
curl -s -o /dev/null -w 'HTTP %{http_code}\n' "$SITE_ROOT/blog/$slug/"
echo "Open in your browser: $SITE_ROOT/blog/$slug/"
