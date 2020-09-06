# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin

from generic_links.models import GenericLink


class GenericLinkStackedInline(ct_admin.GenericStackedInline):
    model = GenericLink
    extra = 1


class GenericLinkTabularInline(ct_admin.GenericTabularInline):
    model = GenericLink
    extra = 1


@admin.register(GenericLink)
class GenericLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "description", "created_at", "user", "is_external")
    search_fields = ('title', 'url', 'user')
    list_filter = ('is_external', 'created_at', )
    raw_id_fields = ('user', )
