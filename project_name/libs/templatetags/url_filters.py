# encoding: utf-8

from django import template
from django.http import QueryDict

from libs.url_utils import canonical_url

register = template.Library()

@register.filter
def canonical(url):
    return canonical_url(url)
