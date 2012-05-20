# -*- coding: utf-8 -*-
from django.contrib import admin

from generic_links.models import GenericLink


class GenericLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "description", "created_at", "user", "is_external")
    search_fields = ('title', 'url', 'user')
    list_filter = ('is_external', 'created_at', )
    # hoping you have a lot of users
    raw_id_fields = ('user', )


admin.site.register(GenericLink, GenericLinkAdmin)
