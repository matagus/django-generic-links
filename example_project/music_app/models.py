from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    # This is important so that we can get the GenericLink related instances for an object of this model
    # See https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/#reverse-generic-relations
    generic_links = GenericRelation("generic_links.GenericLink")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"
