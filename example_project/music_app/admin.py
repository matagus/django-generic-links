from django.contrib import admin

from generic_links.admin import GenericLinkStackedInline
from music_app.models import Album, Artist


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "artist", "release_date", "created_at", "updated_at"]
    list_filter = ["artist"]
    search_fields = ["title", "artist__name"]
    list_per_page = 10
    inlines = [GenericLinkStackedInline]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    list_per_page = 10
    inlines = [GenericLinkStackedInline]
