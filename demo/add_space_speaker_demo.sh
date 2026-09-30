#!/usr/bin/env bash
#
# Demo/test: append a "speaker_highlight" block containing one speaker to the
# Wagtail Space Speakers page via the Wagtail 8.0 REST API v3 write API.
#
# The speaker's image is uploaded through the write API (POST /images/), the
# page is resolved by name or front-end path through the authenticated
# /pages/ list (which, unlike /pages/find/, also includes draft-only pages),
# the current draft body is fetched, the new block is appended to it, and the
# complete body is PATCHed back (StreamField updates always replace the whole
# value, so the fetched blocks are preserved).
#
# Requires: curl, jq
#
# Usage:
#   TOKEN=wagtail_xxx ./add_space_speaker_demo.sh
#   TOKEN=wagtail_xxx PAGE_TITLE="Speakers" ./add_space_speaker_demo.sh
#   TOKEN=wagtail_xxx PAGE_PATH=/wagtail-space-2025/speakers/ ./add_space_speaker_demo.sh
#   TOKEN=wagtail_xxx PAGE_ID=1523 ./add_space_speaker_demo.sh
#   TOKEN=wagtail_xxx PUBLISH=true ./add_space_speaker_demo.sh
#
# TOKEN       API token from `./manage.py api_tokens create --user=<you> --name=demo`
# API_ROOT    v3 API root (defaults to http://localhost:8000/api/v3-preview)
# SITE_ROOT   front-end URL (defaults to http://localhost:8000)
# PAGE_TITLE  page name, matched exactly against wagtailspace.WagtailSpacePage
#             titles (defaults to "Speakers"). Works for draft-only pages.
# PAGE_PATH   front-end path of the page (defaults to
#             /wagtail-space-2026/speakers/). Disambiguates same-named pages,
#             or is used for lookup when PAGE_TITLE is blank. Also works for
#             draft-only pages.
# PAGE_ID     optional: skip name/path resolution entirely
# PUBLISH     "true" publishes the page as part of the PATCH (default: draft)
# COLLECTION_ID  collection the image is uploaded into (defaults to 1, the
#             root collection; e.g. 5 = "Author Photos", 6 = "Event Photos")
#
# Speaker data: edit the SPEAKER DATA section in this file, then run. The
# speaker name, image file and alt text are required by the speaker block, so
# the script refuses to run while they are blank.

set -euo pipefail

API_ROOT="${API_ROOT:-http://localhost:8000/api/v3-preview}"
SITE_ROOT="${SITE_ROOT:-http://localhost:8000}"
PAGE_TITLE="${PAGE_TITLE:-Speakers}"
PAGE_PATH="${PAGE_PATH:-/wagtail-space-2026/speakers/}"
PUBLISH="${PUBLISH:-false}"
COLLECTION_ID="${COLLECTION_ID:-1}" # collection for the uploaded image (1 = root)

# ---------------------------------------------------------------------------
# SPEAKER DATA - edit these lines, then run the script.
# ---------------------------------------------------------------------------

SPEAKER_HEADING=""     # optional heading above the speakers
SPEAKER_NAME="Meagen Voss"        # required, e.g. "Ada Lovelace"
SPEAKER_IMAGE_FILE="./demo/mvoss-headshot-web.jpg"  # required, path to a local image file, e.g. ./speaker.jpg
SPEAKER_IMAGE_TITLE="" # optional title in the admin (defaults to the alt text)
SPEAKER_IMAGE_ALT="A headshot of Meagen Voss. She is a white woman with brown hair and blue eyes wearing glasses."   # required, e.g. "Portrait of Ada Lovelace"
SPEAKER_TALK="Wagtail Community Manager, Torchbox"        # optional talk title (max 255 chars)
SPEAKER_URL=""         # optional talk URL

: "${TOKEN:?Set TOKEN to an API token (see: ./manage.py api_tokens create --user=<you> --name=demo)}"

auth=(-H "Authorization: Bearer $TOKEN")

step() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }

# ---------------------------------------------------------------------------
# 0. Check the required speaker data has been filled in
# ---------------------------------------------------------------------------

missing=""
[[ -z "$SPEAKER_NAME" ]] && missing+=$'\n  - SPEAKER_NAME (e.g. SPEAKER_NAME="Ada Lovelace")'
[[ -z "$SPEAKER_IMAGE_FILE" ]] && missing+=$'\n  - SPEAKER_IMAGE_FILE (e.g. SPEAKER_IMAGE_FILE="./speaker.jpg", uploaded via the API)'
[[ -z "$SPEAKER_IMAGE_ALT" ]] && missing+=$'\n  - SPEAKER_IMAGE_ALT (e.g. SPEAKER_IMAGE_ALT="Portrait of Ada Lovelace")'

if [[ -n "$missing" ]]; then
    printf 'Missing required speaker data:%s\n' "$missing"
    printf '\nEdit the SPEAKER DATA section at the top of this file, then run again:\n'
    printf '  TOKEN=wagtail_xxx ./add_space_speaker_demo.sh\n'
    exit 1
fi

if [[ ! -f "$SPEAKER_IMAGE_FILE" ]]; then
    echo "SPEAKER_IMAGE_FILE does not point to a readable file (got: \"$SPEAKER_IMAGE_FILE\")"
    exit 1
fi

# ---------------------------------------------------------------------------
# 1. Confirm the token works (whoami)
# ---------------------------------------------------------------------------

curl -sf "${auth[@]}" "$API_ROOT/whoami/" >/dev/null || {
    echo "Token rejected by $API_ROOT/whoami/ - check TOKEN."
    exit 1
}
echo "Token OK"

# ---------------------------------------------------------------------------
# 2. Resolve the target page (by id, by name, or by front-end path)
# ---------------------------------------------------------------------------
#
# Draft-only pages can't be resolved through /pages/find/ (it only serves
# live pages), so this uses the authenticated /pages/ list instead: it
# includes drafts, and each result carries its front-end path in
# meta.html_url - which lets us match by name, by path, or both.

if [[ -n "${PAGE_ID:-}" ]]; then
    page_id="$PAGE_ID"
    echo "Using PAGE_ID=$page_id"
else
    PAGE_PATH="/${PAGE_PATH#/}"                          # ensure leading slash
    [[ "$PAGE_PATH" == */ ]] || PAGE_PATH="$PAGE_PATH/"  # ensure trailing slash

    if [[ -n "$PAGE_TITLE" ]]; then
        lookup=(--data-urlencode "title=$PAGE_TITLE")
    else
        slug="$(printf '%s' "$PAGE_PATH" | sed -E 's#^/+##; s#/+$##; s#.*/##')"
        lookup=(--data-urlencode "slug=$slug")
    fi
    lookup+=(--data-urlencode "type=wagtailspace.WagtailSpacePage")

    list_json=$(curl -sf "${auth[@]}" --get "${lookup[@]}" "$API_ROOT/pages/") || {
        echo "Page lookup at $API_ROOT/pages/ failed."
        exit 1
    }

    candidates=$(echo "$list_json" | jq '[
        .items[]
        | {id, title, path: ((.meta.html_url // "") | sub("^[a-zA-Z][a-zA-Z0-9+.-]*://[^/]*"; ""))}
    ]')

    # Same-named pages (e.g. past events) are disambiguated by front-end path.
    if [[ "$(echo "$candidates" | jq 'length')" -gt 1 && -n "$PAGE_PATH" ]]; then
        narrowed=$(echo "$candidates" | jq --arg path "$PAGE_PATH" \
            '[.[] | select(.path == $path)]')
        [[ "$(echo "$narrowed" | jq 'length')" -ge 1 ]] && candidates="$narrowed"
    fi

    case "$(echo "$candidates" | jq 'length')" in
        0)
            echo "No wagtailspace.WagtailSpacePage matched (title: \"${PAGE_TITLE:-<any>}\", path: \"$PAGE_PATH\")."
            echo "Check PAGE_TITLE / PAGE_PATH, or pass the page id directly: PAGE_ID=<id>"
            exit 1
            ;;
        1)
            page_id="$(echo "$candidates" | jq -r '.[0].id')"
            resolved_path="$(echo "$candidates" | jq -r '.[0].path')"
            echo "Resolved \"$(echo "$candidates" | jq -r '.[0].title')\" at $resolved_path to page id=$page_id"
            ;;
        *)
            echo "Several pages matched - pass PAGE_ID to choose one:"
            echo "$candidates" | jq -r '.[] | "  PAGE_ID=\(.id)  \(.title)  \(.path)"'
            exit 1
            ;;
    esac
fi

# ---------------------------------------------------------------------------
# 3. Fetch the current draft body
# ---------------------------------------------------------------------------

page_json=$(curl -sf "${auth[@]}" "$API_ROOT/pages/$page_id/?version=draft")
body=$(echo "$page_json" | jq '.body // []')

echo "Current body has $(echo "$body" | jq 'length') block(s): $(echo "$body" | jq -r 'map(.type) | join(", ")')"

# ---------------------------------------------------------------------------
# 4. Upload the speaker image (POST /images/, multipart/form-data)
# ---------------------------------------------------------------------------

image_title="${SPEAKER_IMAGE_TITLE:-$SPEAKER_IMAGE_ALT}"
[[ -n "$image_title" ]] || image_title="$(basename "$SPEAKER_IMAGE_FILE")"

upload_fields=(-F "file=@$SPEAKER_IMAGE_FILE" -F "title=$image_title")
[[ -n "$COLLECTION_ID" ]] && upload_fields+=(-F "collection_id=$COLLECTION_ID")

response=$(curl -s "${auth[@]}" "${upload_fields[@]}" \
    -X POST "$API_ROOT/images/" -w '\n%{http_code}')
http_code="${response##*$'\n'}"
response_body="${response%$'\n'*}"

if [[ "$http_code" != "201" && "$http_code" != "200" ]]; then
    echo "Image upload failed (HTTP $http_code):"
    echo "$response_body" | jq .
    exit 1
fi

image_id=$(echo "$response_body" | jq -r '.id')
echo "Uploaded \"$image_title\" as image id=$image_id"

# ---------------------------------------------------------------------------
# 5. Build the speaker_highlight block (one speaker) and append it
# ---------------------------------------------------------------------------

new_block=$(jq -n \
    --arg heading "$SPEAKER_HEADING" \
    --arg name "$SPEAKER_NAME" \
    --argjson image_id "$image_id" \
    --arg alt "$SPEAKER_IMAGE_ALT" \
    --arg talk "$SPEAKER_TALK" \
    --arg url "$SPEAKER_URL" \
    '{
        type: "speaker_highlight",
        value: {
            heading: $heading,
            speaker: [{
                speaker_image: {image: $image_id, alt_text: $alt},
                speaker_name: $name,
                speaker_talk: $talk,
                speaker_url: $url
            }]
        }
    }')

updated_body=$(jq -n --argjson old "$body" --argjson block "$new_block" '$old + [$block]')

if [[ "$PUBLISH" == "true" ]]; then
    payload=$(jq -n --argjson body "$updated_body" '{meta: {action: "publish"}, body: $body}')
else
    payload=$(jq -n --argjson body "$updated_body" '{body: $body}')
fi

# ---------------------------------------------------------------------------
# 6. PATCH the page with the complete body
# ---------------------------------------------------------------------------

response=$(curl -s "${auth[@]}" -H "Content-Type: application/json" \
    -X PATCH "$API_ROOT/pages/$page_id/" -d "$payload" \
    -w '\n%{http_code}')
http_code="${response##*$'\n'}"
response_body="${response%$'\n'*}"

if [[ "$http_code" != "200" ]]; then
    echo "PATCH failed (HTTP $http_code):"
    echo "$response_body" | jq .
    exit 1
fi

echo "$response_body" | jq '{id, title, slug: .meta.slug, blocks: (.body | length), types: (.body | map(.type))}'

# ---------------------------------------------------------------------------
# 7. Done
# ---------------------------------------------------------------------------

if [[ "$PUBLISH" == "true" ]]; then
    echo "Published. View it at: $SITE_ROOT$PAGE_PATH"
else
    echo "Saved as a draft revision. Review and publish it in the admin:"
    echo "  $SITE_ROOT/admin/pages/$page_id/edit/"
fi
