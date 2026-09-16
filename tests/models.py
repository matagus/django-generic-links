from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class TaggedItem(models.Model):
    """Test model with a reverse generic relation, like the README recommends."""

    name = models.CharField(max_length=50)
    generic_links = GenericRelation("generic_links.GenericLink")

    def __str__(self):
        return self.name
