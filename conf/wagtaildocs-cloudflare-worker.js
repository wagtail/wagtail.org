/* eslint-disable */
/*
docs.wagtail.org canonical URL rewriter

This script is installed as a Cloudflare worker on docs.wagtail.org to ensure that the
<link rel="canonical"> tag on all pages is pointing to the 'stable' version of the docs.
Certain older versions of the docs were built at a time when the 'default' version set
on readthedocs was pointing to the specific then-current release, and due to changes in
the readthedocs build environment or external dependencies, cannot be rebuilt without
deleting and recreating the corresponding tags in Wagtail's git repo. As a result, the
stale 'canonical' links persist, leading to search engines prioritising the older
versions over the current stable one.
*/

// The hostname we will fetch documentation pages from. This is configured in readthedocs
// as an alternative (non-default) hostname with HTTPS disabled; this avoids any issues
// with the docs.wagtail.org DNS and SSL certificate being handled by us vs. readthedocs.
const originDomain = 'docs-internal.wagtail.org';

// The hostname that incoming requests will come in on
const proxyDomain = 'docs.wagtail.org';

const originRoot = 'http://' + originDomain + '/';
const proxyRoot = 'https://' + proxyDomain + '/';

addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request));
});

class CanonicalLinkHandler {
  element(element) {
    const oldUrl = element.getAttribute('href');
    // Rewrite any URL paths within /latest/ or /vN.N/ to the corresponding path in /stable/
    const newUrl = oldUrl.replace(
      /^(https?\:\/\/docs\.wagtail\.org\/\w+)\/(v[\d\.]+|latest)\//,
      '$1/stable/',
    );
    element.setAttribute('href', newUrl);
  }
}

/* Respond to the request */
async function handleRequest(request) {
  // Fetch from the origin host
  const originUrl = request.url.replace(proxyRoot, originRoot);
  const resp = await fetch(originUrl, { redirect: 'manual' });

  const location = resp.headers.get('Location');
  const contentType = resp.headers.get('Content-Type');

  if (location) {
    // Rewrite redirect headers to use the proxy domain instead of the origin
    const newResp = new Response(resp.body, {
      status: resp.status,
      statusText: resp.statusText,
      headers: resp.headers,
    });
    newResp.headers.set('Location', location.replace(originRoot, proxyRoot));
    return newResp;
  } else if (contentType && contentType.split(';')[0].endsWith('html')) {
    // Rewrite responses with an html content type
    return new HTMLRewriter()
      .on('link[rel="canonical"]', new CanonicalLinkHandler())
      .transform(resp);
  } else {
    return resp;
  }
}
