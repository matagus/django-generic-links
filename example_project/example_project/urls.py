"""
URL configuration for example_project project.

The `README` documentation lives at https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Public pages that render the links attached with the {% get_links_for %} template tag
    path("", include("music_app.urls")),
]
