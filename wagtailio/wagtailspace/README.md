# Archiving Wagtail Space subsites

Our goal is to archive Wagtail Space sites to sort of "static" versions so we can modify the color
scheme and design each year without changing the pages for previous years. The scripts
for this include mirror-wagtail-space.sh and rearrange-files.py

We start by pulling down all the assets using `wget` and its mirroring options. This will create a
directory containing the content - but because we serve the pages as urls with trailing slashes,
wget will have converted them into directories with an index.html file in each directory. We want to
retain the same urls as we have when serving the pages from the Wagtail CMS so we will need to use a
Django view with a url mapping to have the url path /wagtail-space-2025/somename/ display the html
file /wagtail-space-2025/somename/index.html. The WagtailSpace2025View to do this remapping can be
found in wagtail.org/wagtailio/wagtailspace/views.py

The wget mirroring process will have helpfully converted all the links to match the static directory
structure, so we will need to converted them back to their trailing slash equivalents.

Processing steps - in rearrange-files.py command:

Copy images from media.wagtail.org into
wagtail.org/wagtailio/wagtailspace/static/wagtailspace/images/wagtailspace-2025 then move the ones
used in the design / css into
wagtail.org/wagtailio/wagtailspace/static/wagtailspace/img/wagtailspace-2025

1. Add {% load static manifest %} to the top of each index.html file

2. Convert <script src="../static/js/blocking.4c0750407486.js"></script> to {% manifest blocking.js
   %} and same thing for main.e26c5749797f.js

3. Static image conversions - logos, design elements

src="../static/img/wagtail-space-stars.5cff62d52545.png" src="{% static 'img/wagtail-space-stars.png' %}"

and images that would be in images section of the CMS

src="../../media.wagtail.org/images/Thibaud_Colas-square.max-315x315.jpg"
src="{% static 'wagtailspace/images/wagtailspace-2025/Thibaud_Colas-square.max-315x315.jpg' %}"

5. Convert all the navigation links back from /thing/index.html to /thing/

---

Run the precommit hooks for this project so you can submit a pull request with the
processed files.

---

I got fed up trying to write regex to do all the processing so did a final pass to make
substitutions using my text editor. Those included:

1. Replacing the evaluated favicons with their equivalent code from base_page.html
    <link rel="icon" href="{% static 'img/favicons/favicon.ico' %}" sizes="32x32">
    <link rel="icon" href="{% static 'img/favicons/favicon.sgv' %}" type="image/svg+xml">
    <link rel="apple-touch-icon" href="{% static 'img/favicons/apple-touch-icon.png' %}">
    <link rel="manifest" href="{% static 'img/favicons/favicon.webmanifest' %}">

2. Replace skip to main content index.html#main-content link with #main-content

3. Replace link to Wagtail Space homepage
   <a href="../index.html" aria-label="Wagtail.org homepage">
   <a href="{% url 'wagtail-space-2025' %}" aria-label="Wagtail Space 2025 homepage">

4. Checking all the canonical url relationships and editing as needed

5. Search for index.html - this found links inside pages, e.g. to Code of Conduct and
   Terms and Conditions pages. Also same page links in primary nav.

6. Fix font and image links inside the wagtailspace-2025.css file
