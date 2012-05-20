# -*- coding: UTF-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GenericLink(models.Model):
    """
    Relates an object with an url and its data
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey()

    url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)

    user = models.ForeignKey("auth.User", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    is_external = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ("-created_at", )
        verbose_name = _("Generic Link")
        verbose_name_plural = _("Generic Links")

    def __unicode__(self):
        return self.url
