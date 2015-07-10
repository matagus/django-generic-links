# -*- coding: utf-8 -*-
try:
    # Django 1.6
    from django.conf.urls import patterns, url
except ImportError:
    # Django < 1.6
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('generic_links.views',
    url(r'^(?P<app_model>.*?)/(?P<object_id>\d+)/links/add/$',
        "add_link", name="generic_links_add_link"),
)

