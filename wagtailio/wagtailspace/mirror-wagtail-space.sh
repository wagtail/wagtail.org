#! /bin/bash

# Check for argument
if [ -z "$1" ]; then
  echo "Usage: $0 <subdirectory>"
  exit 1
fi

subdir="$1"
includedirs="$subdir,static,images"
domain="wagtail.org"
domains="$domain,media.wagtail.org"

echo "Starting spider of $domain"

wget \
     --recursive \
     --page-requisites \
     --adjust-extension \
     --span-hosts \
     --convert-links \
     --domains=$domains \
     --include $includedirs \
     --no-parent \
     --execute robots=off \
         "$domain/$subdir" # The URL to download

### Options above explained

# wget \
#      --recursive \ # Download the whole site.
#      --page-requisites \ # Get all assets/elements (CSS/JS/images).
#      --adjust-extension \ # Save files with .html on the end.
#      --span-hosts \ # Include necessary assets from offsite as well.
#      --convert-links \ # Update links to still work in the static version.
#      --domains yoursite.com \ # Do not follow links outside this domain.
#      --include $subdir,static,images \ # Only save files from the specified directories.
#      --no-parent \ # Don't follow links outside the directory you pass in.
#      --execute robots=off \ # Ignore robots.txt
#          yoursite.com/whatever/path # The URL to download

# If you need to debug what is and is not being saved, add --rejected-log=rejected.log
