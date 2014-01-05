# encoding: utf-8

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class MissingImage(object):
    def __init__(self, name=None):
        self.name = name if name else settings.MISSING_IMAGE_URL

class TrackingCreateMixin(models.Model):
    date_created = models.DateTimeField(_(u"Date création"), auto_now_add=True)

    class Meta:
        abstract = True

class TrackingUpdateMixin(models.Model):
    date_updated = models.DateTimeField(_(u"Date mise à jour"), auto_now=True, db_index=True)   # This field is used by Haystack to reindex search

    class Meta:
        abstract = True

class TrackingCreateAndUpdateMixin(TrackingCreateMixin, TrackingUpdateMixin, models.Model):
    class Meta:
        abstract = True
