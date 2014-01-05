# encoding: utf-8

import os

from django.conf import settings
from django.contrib.sites.models import Site

from purl import URL


def canonical_url(url, domain_check=True):
    """
    Ensure that the url contains the `http://mysite.com` part,
    particularly for requests made on the local dev server
    """
    current_site = Site.objects.get(id=settings.SITE_ID)
    if not url.startswith('http'):
        url = "http://%s" % os.path.join(current_site.domain, url.lstrip('/'))
    
    if domain_check:
        url_parts = URL(url)
        current_site_parts = URL(URL().domain(current_site.domain).as_string())
        if url_parts.subdomains()[-2:] != current_site_parts.subdomains()[-2:]:
            raise ValueError("Suspicious domain '%s' that differs from the "
                "current Site one '%s'" % (url_parts.domain(), current_site_parts.domain()))

    return url

def url_signature(resolver_match):
    """
    Convert 
        a `django.core.urlresolvers.ResolverMatch` instance 
        usually retrieved from a `django.core.urlresolvers.resolve` call
    To 
        'namespace:view_name'

    that `django.core.urlresolvers.reverse` can use
    """
    signature = resolver_match.url_name
    if resolver_match.namespace:
        signature = "%s:%s" % (resolver_match.namespace, signature)
    return signature